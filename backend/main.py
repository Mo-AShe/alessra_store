import os
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Query, Body, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

raw_url = os.getenv("SUPABASE_URL", "https://gqwozzimuetdxgcsdgfg.supabase.co")
if "/rest/v1" in raw_url:
    raw_url = raw_url.split("/rest/v1")[0]
if "/auth/v1" in raw_url:
    raw_url = raw_url.split("/auth/v1")[0]
SUPABASE_URL = raw_url.rstrip("/")

SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", os.getenv("SUPABASE_PUBLISHABLE_KEY", "sb_secret_YMduGoOwPVmDIUFdy_f8iQ_sZVWYqrQ"))

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="محل الاسراء - FastAPI Backend",
    description="FastAPI Backend powered by Supabase PostgreSQL for Al-Esraa Plumbing Store",
    version="1.0.0"
)
@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"DEBUG REQ: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# ==================== PYDANTIC SCHEMAS ====================

class ProductCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str
    code: str
    category: str
    buyPrice: float = Field(..., alias="buyPrice")
    sellPrice: float = Field(..., alias="sellPrice")
    stock: int
    minStock: int = Field(10, alias="minStock")

class ProductResponse(BaseModel):
    id: int
    name: str
    code: str
    category: str
    buyPrice: float
    sellPrice: float
    stock: int
    minStock: int

class CustomerCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str
    phone: Optional[str] = ""
    totalPurchases: float = Field(0, alias="totalPurchases")
    paid: float = 0
    status: Optional[str] = "paid"

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    totalPurchases: float
    paid: float
    status: str

class CartItemSchema(BaseModel):
    id: int
    name: str
    price: float
    qty: int
    category: Optional[str] = None
    maxStock: Optional[int] = None

class CheckoutRequest(BaseModel):
    cart: List[CartItemSchema]
    discount: float = 0
    selectedCustomerId: Optional[int] = None

class TransactionResponse(BaseModel):
    id: int
    invoiceNo: str
    time: str
    date: str
    customerName: str
    productName: str
    amount: float
    status: str

class UserCreate(BaseModel):
    email: str
    password: Optional[str] = None
    name: str
    role: str
    roleCode: str
    permissions: List[str] = []
    status: str = "active"

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    roleCode: str
    permissions: List[str] = []
    status: str = "active"

class LoginRequest(BaseModel):
    email: str
    password: str

class ShopSettingsSchema(BaseModel):
    shop: Dict[str, str]
    invoice: Dict[str, Any]
    currency: str = "EGP"
    dateFormat: str = "ar-EG"
    timezone: str = "Africa/Cairo"

# ==================== INITIAL DATA FOR SEEDING ====================

INITIAL_PRODUCTS = [
    {"name": "خلاط مياه حوض نيكل استانلس", "code": "P-101", "category": "خلاطات", "buy_price": 450, "sell_price": 650, "stock": 25, "min_stock": 5, "is_active": True},
    {"name": "محبس دفن 3/4 بوصة إيطالي", "code": "P-102", "category": "محابس ومحولات", "buy_price": 85, "sell_price": 130, "stock": 40, "min_stock": 10, "is_active": True},
    {"name": "ماسورة بولي بروبلين 1 بوصة (4 متر)", "code": "P-103", "category": "مواسير ووصلات", "buy_price": 120, "sell_price": 175, "stock": 60, "min_stock": 15, "is_active": True},
    {"name": "سيفون حوض بلاستيك مرن 1.5 بوصة", "code": "P-104", "category": "صرف صحي", "buy_price": 35, "sell_price": 55, "stock": 8, "min_stock": 10, "is_active": True},
    {"name": "شاطوف حمام كروم مع خرطوم 1.2 متر", "code": "P-105", "category": "خلاطات", "buy_price": 110, "sell_price": 180, "stock": 30, "min_stock": 8, "is_active": True},
    {"name": "شريط تفلون مانع للتسريب (علبة 10 قطع)", "code": "P-106", "category": "مستلزمات عامة", "buy_price": 40, "sell_price": 65, "stock": 50, "min_stock": 12, "is_active": True},
    {"name": "محبس زاوي 1/2 بوصة اسباني", "code": "P-107", "category": "محابس ومحولات", "buy_price": 50, "sell_price": 85, "stock": 4, "min_stock": 10, "is_active": True},
    {"name": "سخان مياه كهربائي 50 لتر", "code": "P-108", "category": "أجهزة وسخانات", "buy_price": 2800, "sell_price": 3400, "stock": 6, "min_stock": 2, "is_active": True},
]

INITIAL_CUSTOMERS = [
    {"name": "الشركة الهندسية للمقاولات", "phone": "010-1234-5678", "total_purchases": 0, "paid": 0, "status": "paid", "is_active": True},
    {"name": "معلم أحمد السباك", "phone": "011-9876-5432", "total_purchases": 0, "paid": 0, "status": "paid", "is_active": True},
    {"name": "مكتب الأمل للتصميمات", "phone": "012-5555-4444", "total_purchases": 0, "paid": 0, "status": "paid", "is_active": True},
    {"name": "المهندس محمود حسن", "phone": "015-3333-2222", "total_purchases": 0, "paid": 0, "status": "paid", "is_active": True}
]

INITIAL_USERS = [
    {"name": "أحمد إبراهيم", "email": "admin@al-esraa.com", "role_code": "admin", "password_hash": "admin123", "is_active": True},
    {"name": "محمد علي", "email": "employee@al-esraa.com", "role_code": "employee", "password_hash": "emp123", "is_active": True},
    {"name": "خالد سعيد", "email": "inventory@al-esraa.com", "role_code": "employee", "password_hash": "inv123", "is_active": False}
]

DEFAULT_SETTINGS = {
    "shop_name": "محل الاسراء لأدوات السباكة",
    "shop_address": "مصر - القاهرة - مدينة نصر",
    "shop_phone": "012-3456-7890",
    "shop_email": "info@al-esraa.com",
    "currency": "EGP",
    "date_format": "ar-EG",
    "timezone": "Africa/Cairo",
    "default_discount": 0,
    "default_tax": 14,
    "invoice_start_number": 1,
    "print_copies": 1,
    "show_tax": True,
    "show_discount": True
}

# ==================== ENDPOINTS ====================

@app.get("/api/health")
def health_check():
    return {"status": "ok", "database": "supabase", "url": SUPABASE_URL}

@app.post("/api/seed")
def seed_database():
    """Ensure shop settings, users, products, and customers exist in Supabase if empty."""
    results = {}
    try:
        # Settings
        sett_res = supabase.table("settings").select("*").execute()
        if len(sett_res.data) == 0:
            supabase.table("settings").insert([DEFAULT_SETTINGS]).execute()
            results["settings"] = "Seeded shop settings"
        else:
            results["settings"] = "Already has settings"

        # Users
        u_res = supabase.table("users").select("*").execute()
        if len(u_res.data) == 0:
            supabase.table("users").insert(INITIAL_USERS).execute()
            results["users"] = f"Seeded {len(INITIAL_USERS)} default users"
        else:
            results["users"] = "Already has users"

        # Products
        p_res = supabase.table("products").select("*").execute()
        if len(p_res.data) == 0:
            supabase.table("products").insert(INITIAL_PRODUCTS).execute()
            results["products"] = f"Seeded {len(INITIAL_PRODUCTS)} default products"
        else:
            results["products"] = "Already has products"

        # Customers
        c_res = supabase.table("customers").select("*").execute()
        if len(c_res.data) == 0:
            supabase.table("customers").insert(INITIAL_CUSTOMERS).execute()
            results["customers"] = f"Seeded {len(INITIAL_CUSTOMERS)} default customers"
        else:
            results["customers"] = "Already has customers"

        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed database: {str(e)}")

# --- PRODUCTS ---

@app.get("/api/products")
def get_products():
    try:
        res = supabase.table("products").select("*").order("id", desc=True).execute()
        mapped = []
        for row in res.data:
            mapped.append({
                "id": row["id"],
                "name": row["name"],
                "code": row["code"],
                "category": row["category"],
                "buyPrice": row.get("buy_price", 0),
                "sellPrice": row.get("sell_price", 0),
                "stock": row.get("stock", 0),
                "minStock": row.get("min_stock", 10),
            })
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/products")
def create_product(product: ProductCreate):
    try:
        payload = {
            "name": product.name,
            "code": product.code,
            "category": product.category,
            "buy_price": product.buyPrice,
            "sell_price": product.sellPrice,
            "stock": product.stock,
            "min_stock": product.minStock,
            "is_active": True
        }
        res = supabase.table("products").insert(payload).execute()
        if res.data and len(res.data) > 0:
            row = res.data[0]
            return {
                "id": row["id"],
                "name": row["name"],
                "code": row["code"],
                "category": row["category"],
                "buyPrice": row.get("buy_price", 0),
                "sellPrice": row.get("sell_price", 0),
                "stock": row.get("stock", 0),
                "minStock": row.get("min_stock", 10),
            }
        raise HTTPException(status_code=400, detail="Failed to insert product")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/products/{product_id}")
def update_product(product_id: int, product: ProductCreate):
    try:
        payload = {
            "name": product.name,
            "code": product.code,
            "category": product.category,
            "buy_price": product.buyPrice,
            "sell_price": product.sellPrice,
            "stock": product.stock,
            "min_stock": product.minStock
        }
        res = supabase.table("products").update(payload).eq("id", product_id).execute()
        if res.data and len(res.data) > 0:
            row = res.data[0]
            return {
                "id": row["id"],
                "name": row["name"],
                "code": row["code"],
                "category": row["category"],
                "buyPrice": row.get("buy_price", 0),
                "sellPrice": row.get("sell_price", 0),
                "stock": row.get("stock", 0),
                "minStock": row.get("min_stock", 10),
            }
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    try:
        res = supabase.table("products").delete().eq("id", product_id).execute()
        return {"status": "success", "deleted_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- CUSTOMERS ---

@app.get("/api/customers")
def get_customers():
    try:
        res = supabase.table("customers").select("*").order("id", desc=True).execute()
        mapped = []
        for row in res.data:
            mapped.append({
                "id": row["id"],
                "name": row["name"],
                "phone": row.get("phone", ""),
                "totalPurchases": row.get("total_purchases", 0),
                "paid": row.get("paid", 0),
                "status": row.get("status", "paid")
            })
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/customers")
def create_customer(customer: CustomerCreate):
    try:
        payload = {
            "name": customer.name,
            "phone": customer.phone,
            "total_purchases": customer.totalPurchases,
            "paid": customer.paid,
            "status": customer.status,
            "is_active": True
        }
        res = supabase.table("customers").insert(payload).execute()
        if res.data and len(res.data) > 0:
            row = res.data[0]
            return {
                "id": row["id"],
                "name": row["name"],
                "phone": row.get("phone", ""),
                "totalPurchases": row.get("total_purchases", 0),
                "paid": row.get("paid", 0),
                "status": row.get("status", "paid")
            }
        raise HTTPException(status_code=400, detail="Failed to insert customer")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerCreate):
    try:
        payload = {
            "name": customer.name,
            "phone": customer.phone,
            "total_purchases": customer.totalPurchases,
            "paid": customer.paid,
            "status": customer.status
        }
        res = supabase.table("customers").update(payload).eq("id", customer_id).execute()
        if res.data and len(res.data) > 0:
            row = res.data[0]
            return {
                "id": row["id"],
                "name": row["name"],
                "phone": row.get("phone", ""),
                "totalPurchases": row.get("total_purchases", 0),
                "paid": row.get("paid", 0),
                "status": row.get("status", "paid")
            }
        raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/customers/{customer_id}")
def delete_customer(customer_id: int):
    try:
        supabase.table("customers").delete().eq("id", customer_id).execute()
        return {"status": "success", "deleted_id": customer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- TRANSACTIONS & CHECKOUT ---

@app.get("/api/transactions")
def get_transactions():
    try:
        # Query invoices from Supabase
        res = supabase.table("invoices").select("*").order("id", desc=True).execute()
        mapped = []
        for row in res.data:
            # Get customer name
            c_name = "عميل نقدي"
            if row.get("customer_id"):
                c_res = supabase.table("customers").select("name").eq("id", row["customer_id"]).execute()
                if c_res.data:
                    c_name = c_res.data[0]["name"]
            
            created_dt = row.get("created_at", "")
            date_str = created_dt[:10] if len(created_dt) >= 10 else "اليوم"
            time_str = created_dt[11:16] if len(created_dt) >= 16 else "12:00"

            # Get items summary and total quantity
            p_name = "مستلزمات سباكة"
            total_qty = 0
            items_res = supabase.table("invoice_items").select("product_id, quantity").eq("invoice_id", row["id"]).execute()
            if items_res.data and len(items_res.data) > 0:
                p_id = items_res.data[0]["product_id"]
                p_res = supabase.table("products").select("name").eq("id", p_id).execute()
                if p_res.data:
                    p_name = p_res.data[0]["name"]
                if len(items_res.data) > 1:
                    p_name = f"{p_name} +{len(items_res.data) - 1}"
                total_qty = sum(item.get("quantity", 1) for item in items_res.data)
            else:
                total_qty = 1

            mapped.append({
                "id": row["id"],
                "invoiceNo": row.get("invoice_number", f"INV-{row['id']}"),
                "time": time_str,
                "date": date_str,
                "customerName": c_name,
                "productName": p_name,
                "amount": row.get("total", 0),
                "totalQuantity": total_qty,
                "status": "done" if row.get("status") == "paid" or row.get("status") == "done" else row.get("status", "done")
            })
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/checkout")
def process_checkout(req: CheckoutRequest):
    if not req.cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        # Get count for next invoice number
        inv_count_res = supabase.table("invoices").select("id", count="exact").execute()
        count = inv_count_res.count if inv_count_res.count is not None else 0
        inv_num = f"INV-{str(count + 1).zfill(3)}"

        subtotal = sum(item.price * item.qty for item in req.cart)
        total = max(0, subtotal - req.discount)

        # Validate selectedCustomerId against customers table to prevent foreign key errors
        valid_cust_id = None
        if req.selectedCustomerId and req.selectedCustomerId > 0:
            c_check = supabase.table("customers").select("id").eq("id", req.selectedCustomerId).execute()
            if c_check.data and len(c_check.data) > 0:
                valid_cust_id = req.selectedCustomerId

        # 1. Insert invoice
        inv_payload = {
            "invoice_number": inv_num,
            "customer_id": valid_cust_id,
            "subtotal": subtotal,
            "discount": req.discount,
            "tax": 0,
            "total": total,
            "status": "paid",
            "payment_method": "cash"
        }
        inv_res = supabase.table("invoices").insert(inv_payload).execute()
        if not inv_res.data:
            # Try inserting without customer_id if it fails
            inv_payload["customer_id"] = None
            inv_res = supabase.table("invoices").insert(inv_payload).execute()
            if not inv_res.data:
                raise HTTPException(status_code=500, detail="Failed to create invoice")

        invoice_id = inv_res.data[0]["id"]

        # 2. Insert items and update product stock
        for item in req.cart:
            p_res = supabase.table("products").select("id, stock").eq("id", item.id).execute()
            if p_res.data and len(p_res.data) > 0:
                real_p_id = p_res.data[0]["id"]
                item_payload = {
                    "invoice_id": invoice_id,
                    "product_id": real_p_id,
                    "quantity": item.qty,
                    "unit_price": item.price,
                    "total_price": item.price * item.qty
                }
                try:
                    supabase.table("invoice_items").insert(item_payload).execute()
                except Exception as ie:
                    print(f"Error inserting invoice item: {ie}")

                # Deduct stock
                curr_stock = p_res.data[0].get("stock", 0)
                new_stock = max(0, curr_stock - item.qty)
                try:
                    supabase.table("products").update({"stock": new_stock}).eq("id", real_p_id).execute()
                except Exception as se:
                    print(f"Error updating stock: {se}")

        # 3. Update customer if specified
        if valid_cust_id:
            try:
                c_res = supabase.table("customers").select("total_purchases, paid").eq("id", valid_cust_id).execute()
                if c_res.data:
                    curr_tp = c_res.data[0].get("total_purchases", 0) or 0
                    curr_paid = c_res.data[0].get("paid", 0) or 0
                    supabase.table("customers").update({
                        "total_purchases": curr_tp + total,
                        "paid": curr_paid + total
                    }).eq("id", valid_cust_id).execute()
            except Exception as ce:
                print(f"Error updating customer: {ce}")

        return {"success": True, "invoiceNo": inv_num, "invoiceId": invoice_id}
    except Exception as e:
        print(f"Checkout error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- USERS & AUTH ---

@app.get("/api/users")
def get_users():
    try:
        res = supabase.table("users").select("*").execute()
        mapped = []
        for row in res.data:
            role_code = row.get("role_code", "employee")
            mapped.append({
                "id": row["id"],
                "email": row["email"],
                "name": row["name"],
                "role": "مدير النظام" if role_code == "admin" else "موظف",
                "roleCode": role_code,
                "permissions": ["dashboard", "inventory", "pos", "customers", "reports", "settings", "profile"] if role_code == "admin" else ["dashboard", "pos", "customers", "profile"],
                "status": "active" if row.get("is_active", True) else "inactive"
            })
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
def login_user(login_req: LoginRequest):
    try:
        res = supabase.table("users").select("*").eq("email", login_req.email).execute()
        if res.data:
            u = res.data[0]
            if not u.get("is_active", True):
                raise HTTPException(status_code=403, detail="المستخدم غير نشط")
            
            role_code = u.get("role_code", "employee")
            return {
                "success": True,
                "user": {
                    "id": u["id"],
                    "email": u["email"],
                    "name": u["name"],
                    "role": "مدير النظام" if role_code == "admin" else "موظف",
                    "roleCode": role_code,
                    "permissions": ["dashboard", "inventory", "pos", "customers", "reports", "settings", "profile"] if role_code == "admin" else ["dashboard", "pos", "customers", "profile"],
                    "status": "active"
                }
            }
        raise HTTPException(status_code=401, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users")
def create_user(user: UserCreate):
    try:
        payload = {
            "name": user.name,
            "email": user.email,
            "role_code": user.roleCode,
            "is_active": user.status == "active",
            "password_hash": user.password or "admin123"
        }
        res = supabase.table("users").insert(payload).execute()
        if res.data and len(res.data) > 0:
            u = res.data[0]
            role_code = u.get("role_code", "employee")
            return {
                "id": u["id"],
                "email": u["email"],
                "name": u["name"],
                "role": "مدير النظام" if role_code == "admin" else "موظف",
                "roleCode": role_code,
                "permissions": ["dashboard", "inventory", "pos", "customers", "reports", "settings", "profile"] if role_code == "admin" else ["dashboard", "pos", "customers", "profile"],
                "status": "active" if u.get("is_active", True) else "inactive"
            }
        raise HTTPException(status_code=400, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    try:
        payload = {
            "name": user.name,
            "email": user.email,
            "role_code": user.roleCode,
            "is_active": user.status == "active"
        }
        if user.password:
            payload["password_hash"] = user.password

        res = supabase.table("users").update(payload).eq("id", user_id).execute()
        if res.data and len(res.data) > 0:
            u = res.data[0]
            role_code = u.get("role_code", "employee")
            return {
                "id": u["id"],
                "email": u["email"],
                "name": u["name"],
                "role": "مدير النظام" if role_code == "admin" else "موظف",
                "roleCode": role_code,
                "permissions": ["dashboard", "inventory", "pos", "customers", "reports", "settings", "profile"] if role_code == "admin" else ["dashboard", "pos", "customers", "profile"],
                "status": "active" if u.get("is_active", True) else "inactive"
            }
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{user_id}/status")
def toggle_user_status(user_id: int, payload: Dict[str, Any] = Body(...)):
    try:
        is_active = payload.get("status") == "active"
        supabase.table("users").update({"is_active": is_active}).eq("id", user_id).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{user_id}/profile")
def update_user_profile_api(user_id: int, payload: Dict[str, Any] = Body(...)):
    try:
        supabase.table("users").update({
            "name": payload.get("name"),
            "phone": payload.get("phone")
        }).eq("id", user_id).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{user_id}/password")
def change_user_password_api(user_id: int, payload: Dict[str, Any] = Body(...)):
    try:
        supabase.table("users").update({
            "password_hash": payload.get("newPassword")
        }).eq("id", user_id).execute()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- SETTINGS ---

@app.get("/api/settings")
def get_settings():
    try:
        res = supabase.table("settings").select("*").limit(1).execute()
        if res.data and len(res.data) > 0:
            s = res.data[0]
            return {
                "shop": {
                    "name": s.get("shop_name", "محل الاسراء لأدوات السباكة"),
                    "address": s.get("shop_address", "مصر - القاهرة - مدينة نصر"),
                    "phone": s.get("shop_phone", "012-3456-7890"),
                    "email": s.get("shop_email", "info@al-esraa.com")
                },
                "invoice": {
                    "start": s.get("invoice_start_number", 1),
                    "discount": s.get("default_discount", 0),
                    "tax": s.get("default_tax", 14),
                    "copies": s.get("print_copies", 1),
                    "showTax": s.get("show_tax", True),
                    "showDiscount": s.get("show_discount", True)
                },
                "currency": s.get("currency", "EGP"),
                "dateFormat": s.get("date_format", "ar-EG"),
                "timezone": s.get("timezone", "Africa/Cairo")
            }
        return DEFAULT_SETTINGS
    except Exception as e:
        return DEFAULT_SETTINGS

@app.put("/api/settings")
def update_settings(settings_data: ShopSettingsSchema):
    try:
        payload = {
            "shop_name": settings_data.shop.get("name"),
            "shop_address": settings_data.shop.get("address"),
            "shop_phone": settings_data.shop.get("phone"),
            "shop_email": settings_data.shop.get("email"),
            "invoice_start_number": settings_data.invoice.get("start"),
            "default_discount": settings_data.invoice.get("discount"),
            "default_tax": settings_data.invoice.get("tax"),
            "print_copies": settings_data.invoice.get("copies"),
            "show_tax": settings_data.invoice.get("showTax"),
            "show_discount": settings_data.invoice.get("showDiscount"),
            "currency": settings_data.currency,
            "date_format": settings_data.dateFormat,
            "timezone": settings_data.timezone
        }
        res = supabase.table("settings").select("id").limit(1).execute()
        if res.data:
            sid = res.data[0]["id"]
            supabase.table("settings").update(payload).eq("id", sid).execute()
        else:
            supabase.table("settings").insert(payload).execute()
        return {"status": "success", "message": "Settings updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
