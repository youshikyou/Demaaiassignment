from fastapi import APIRouter, Depends, HTTPException
from models import InventoryQueryParams, InventoryUpdateItem, BulkInventoryUpdate
from database import get_db_connection

# Initialize the APIRouter
router = APIRouter()

# Endpoint to list inventory
@router.get("/inventory/list")
def list_inventory(params: InventoryQueryParams = Depends()):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    base_query = """
        select i.productId, i.name, i.category, i.subCategory, 
               i.quantity as stock, count(o.orderId) as order_count
        from inventory i
        left join orders o on i.productId = o.productId
    """

    where_clauses = []
    params_dict = params.dict()
    query_params = []

    # Filtering conditions
    if params_dict['category']:
        where_clauses.append("i.category = %s")
        query_params.append(params_dict['category'])
    if params_dict['subcategory']:
        where_clauses.append("i.subCategory = %s")
        query_params.append(params_dict['subcategory'])
    if params_dict['in_stock']:
        where_clauses.append("i.quantity > 0")

    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)

    group_by = " GROUP BY i.productId, i.name, i.category, i.subCategory, i.quantity"
    base_query += group_by

    # Sorting conditions
    if params_dict['sort_order'] == 'stock':
        base_query += " ORDER BY i.quantity DESC"
    elif params_dict['sort_order'] == 'orders':
        base_query += " ORDER BY order_count DESC"

    limit_offset = " LIMIT %s OFFSET %s"
    query_params.extend([params_dict['per_page'], (params_dict['page'] - 1) * params_dict['per_page']])
    final_query = base_query + limit_offset

    cursor.execute(final_query, query_params)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

@router.post("/inventory/update")
def update_inventory(bulk_update: BulkInventoryUpdate):
    connection = get_db_connection()
    updated_products = []
    try:
        cursor = connection.cursor(dictionary=True)
        for item in bulk_update.updates:
            # Update each item
            cursor.execute(
                "UPDATE inventory SET quantity = %s WHERE productId = %s",
                (item.quantity, item.productId)
            )
            if cursor.rowcount == 0:
                # If no rows were updated, raise an exception
                raise HTTPException(status_code=404, detail=f"Item not found: {item.productId}")
            
            # Fetch the updated product and its order data
            cursor.execute(
                """SELECT i.productId, i.name, i.category, i.subCategory, i.quantity as stock,
                          o.orderId, o.quantity as orderQuantity, o.dateTime
                   FROM inventory i
                   LEFT JOIN orders o ON i.productId = o.productId
                   WHERE i.productId = %s""",
                (item.productId,)
            )
            updated_info = cursor.fetchall()
            updated_products.append(updated_info)

        # Commit the updates
        connection.commit()

    except mysql.connector.Error as err:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

    return {"success": True, "updated": updated_products}