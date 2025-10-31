from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import logging
from datetime import datetime
import asyncio
import random
from typing import Dict, List, Optional
import hashlib
import jwt

# تنظیمات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🚀 ÆTHERION - سیستم بانکداری هوشمند",
    description="پلتفرم پیشرفته بانکداری دیجیتال با هوش مصنوعی",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# سیستم بانکداری ایرانی
class IranianBankingSystem:
    def __init__(self):
        self.accounts = {}
        self.transactions = []
        self.banks = {
            "melli": "ملی ایران", "mellat": "ملت", "saderat": "صادرات",
            "tejarat": "تجارت", "sepah": "سپه", "keshavarzi": "کشاورزی"
        }
        logger.info("✅ سیستم بانکداری ایرانی راه‌اندازی شد")
    
    def create_account(self, user_id: str, bank_code: str, initial_balance: float = 0) -> Dict:
        if bank_code not in self.banks:
            raise HTTPException(400, "بانک مورد نظر پشتیبانی نمی‌شود")
        
        account_number = f"{bank_code}{random.randint(1000000000, 9999999999)}"
        self.accounts[account_number] = {
            'user_id': user_id,
            'bank_name': self.banks[bank_code],
            'balance': initial_balance,
            'currency': 'IRR',
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        return {"account_number": account_number, "bank": self.banks[bank_code], "balance": initial_balance}
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> Dict:
        if from_account not in self.accounts:
            raise HTTPException(400, "حساب مبدا یافت نشد")
        if to_account not in self.accounts:
            raise HTTPException(400, "حساب مقصد یافت نشد")
        if self.accounts[from_account]['balance'] < amount:
            raise HTTPException(400, "موجودی کافی نیست")
        
        self.accounts[from_account]['balance'] -= amount
        self.accounts[to_account]['balance'] += amount
        
        transaction = {
            'id': len(self.transactions) + 1,
            'from_account': from_account,
            'to_account': to_account,
            'amount': amount,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
        self.transactions.append(transaction)
        return transaction

# سیستم معاملاتی پیشرفته
class AdvancedTradingSystem:
    def __init__(self):
        self.orders = {}
        self.positions = {}
        self.exchanges = {
            'binance': {'name': 'Binance', 'active': True},
            'bingx': {'name': 'BingX', 'active': True},
            'mexc': {'name': 'MEXC', 'active': True},
            'bitpin': {'name': 'Bitpin', 'active': True},
            'okx': {'name': 'OKX', 'active': True}
        }
        logger.info("✅ سیستم معاملاتی پیشرفته راه‌اندازی شد")
    
    async def get_multi_market_data(self, symbol: str) -> Dict:
        market_data = {}
        
        for exchange_id, exchange_info in self.exchanges.items():
            if exchange_info['active']:
                try:
                    base_price = self._get_base_price(symbol)
                    price_change = random.uniform(-0.03, 0.03)
                    current_price = base_price * (1 + price_change)
                    
                    market_data[exchange_id] = {
                        'symbol': symbol,
                        'price': round(current_price, 4),
                        'change': round(price_change * 100, 2),
                        'volume': random.randint(1000, 100000),
                        'timestamp': datetime.now().isoformat(),
                        'high': round(current_price * 1.02, 4),
                        'low': round(current_price * 0.98, 4),
                        'exchange': exchange_info['name']
                    }
                except Exception as e:
                    market_data[exchange_id] = {'error': str(e)}
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'exchanges': market_data,
            'best_bid': self._find_best_bid(market_data),
            'best_ask': self._find_best_ask(market_data)
        }
    
    def _get_base_price(self, symbol: str) -> float:
        prices = {
            'BTCUSDT': 45000, 'ETHUSDT': 2500, 'ADAUSDT': 0.45,
            'DOTUSDT': 6.5, 'IRRUSD': 0.000024, 'XAUUSD': 1950,
            'EURUSD': 1.08, 'GBPUSD': 1.26, 'USDJPY': 148.5
        }
        return prices.get(symbol, 100)
    
    def _find_best_bid(self, market_data: Dict) -> float:
        prices = [data.get('price', 0) for data in market_data.values() if 'price' in data]
        return min(prices) if prices else 0
    
    def _find_best_ask(self, market_data: Dict) -> float:
        prices = [data.get('price', 0) for data in market_data.values() if 'price' in data]
        return max(prices) if prices else 0
    
    async def execute_multi_order(self, symbol: str, side: str, quantity: float) -> Dict:
        results = {}
        
        for exchange_id in self.exchanges.keys():
            try:
                order_result = {
                    'order_id': f"{exchange_id.upper()}_ORDER_{random.randint(100000, 999999)}",
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'status': 'filled',
                    'exchange': exchange_id,
                    'price': self._get_base_price(symbol) * (1 + random.uniform(-0.01, 0.01)),
                    'timestamp': datetime.now().isoformat()
                }
                results[exchange_id] = order_result
            except Exception as e:
                results[exchange_id] = {'error': str(e)}
        
        return {
            'success': True,
            'orders': results,
            'total_quantity': quantity,
            'average_price': sum([order.get('price', 0) for order in results.values() if 'price' in order]) / len(results)
        }

# سیستم امنیتی
class SecuritySystem:
    def __init__(self):
        self.secret_key = "aetherion-secure-key-2024"
        self.algorithm = "HS256"
    
    def create_token(self, user_id: str) -> str:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow().timestamp() + 3600,
            'iat': datetime.utcnow().timestamp()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "توکن منقضی شده است")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "توکن نامعتبر است")

# نمونه‌های سیستم
banking_system = IranianBankingSystem()
trading_system = AdvancedTradingSystem()
security_system = SecuritySystem()

# Routeهای اصلی
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 ÆTHERION</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
            body { background: linear-gradient(135deg, #667eea, #764ba2); color: white; min-height: 100vh; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; text-align: center; }
            .header { margin-bottom: 40px; }
            h1 { font-size: 4em; margin-bottom: 10px; }
            .subtitle { font-size: 1.5em; opacity: 0.9; margin-bottom: 30px; }
            .status { background: #10b981; padding: 15px 30px; border-radius: 25px; display: inline-block; margin: 20px 0; font-size: 1.2em; }
            .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 40px 0; }
            .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; backdrop-filter: blur(10px); }
            .card h3 { margin-bottom: 20px; font-size: 1.4em; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin: 20px 0; }
            .feature { background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; font-size: 0.9em; }
            .button { display: inline-block; background: white; color: #667eea; padding: 12px 25px; margin: 8px; border-radius: 10px; text-decoration: none; font-weight: bold; transition: transform 0.3s; }
            .button:hover { transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 ÆTHERION</h1>
                <div class="subtitle">سیستم بانکداری هوشمند نسل بعدی</div>
                <div class="status">✅ سیستم فعال و آماده به کار - نسخه ۴.۰.۰</div>
            </div>

            <div class="dashboard">
                <div class="card">
                    <h3>🏦 بانکداری ایرانی</h3>
                    <p>سیستم کامل بانکداری مطابق قوانین ایران</p>
                    <div class="features">
                        <div class="feature">شبکه شتاب</div>
                        <div class="feature">پسات</div>
                        <div class="feature">۶ بانک اصلی</div>
                    </div>
                    <a href="/docs#/default/create_account_banking_create_account_post" class="button">ایجاد حساب</a>
                </div>

                <div class="card">
                    <h3>🤖 معاملات هوشمند</h3>
                    <p>ربات معاملاتی با هوش مصنوعی پیشرفته</p>
                    <div class="features">
                        <div class="feature">BingX</div>
                        <div class="feature">Mexc</div>
                        <div class="feature">Bitpin</div>
                    </div>
                    <a href="/docs#/default/get_multi_market_data_api_markets__symbol__get" class="button">داده بازار</a>
                </div>

                <div class="card">
                    <h3>💰 کیف پول چندارزی</h3>
                    <p>پشتیبانی از تمام ارزهای دیجیتال و فیات</p>
                    <div class="features">
                        <div class="feature">بیت‌کوین</div>
                        <div class="feature">اتریوم</div>
                        <div class="feature">تتر</div>
                    </div>
                    <a href="/docs#/default/transfer_funds_api_banking_transfer_post" class="button">انتقال وجه</a>
                </div>
            </div>

            <div>
                <a href="/docs" class="button">📚 مستندات API</a>
                <a href="/health" class="button">🏥 سلامت سیستم</a>
                <a href="/api/markets/BTCUSDT" class="button">📊 بازار BTC</a>
                <a href="/api/banking/banks" class="button">🏦 بانک‌ها</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0",
        "services": {
            "banking": "active",
            "trading": "active", 
            "security": "active",
            "api": "running"
        },
        "message": "✅ سیستم ÆTHERION با موفقیت راه‌اندازی شد"
    })

@app.get("/api/markets/{symbol}")
async def get_multi_market_data(symbol: str):
    data = await trading_system.get_multi_market_data(symbol)
    return JSONResponse(data)

@app.get("/api/banking/banks")
async def get_supported_banks():
    return JSONResponse({
        "banks": banking_system.banks,
        "count": len(banking_system.banks)
    })

@app.post("/api/banking/create_account")
async def create_account(user_id: str, bank_code: str, initial_balance: float = 0):
    try:
        result = banking_system.create_account(user_id, bank_code, initial_balance)
        return JSONResponse({"success": True, "data": result})
    except HTTPException as e:
        return JSONResponse({"success": False, "error": e.detail}, status_code=400)

@app.post("/api/banking/transfer")
async def transfer_funds(from_account: str, to_account: str, amount: float):
    try:
        result = banking_system.transfer(from_account, to_account, amount)
        return JSONResponse({"success": True, "transaction": result})
    except HTTPException as e:
        return JSONResponse({"success": False, "error": e.detail}, status_code=400)

@app.post("/api/trading/order")
async def place_multi_order(symbol: str, side: str, quantity: float):
    result = await trading_system.execute_multi_order(symbol, side, quantity)
    return JSONResponse(result)

@app.post("/api/auth/token")
async def create_auth_token(user_id: str):
    token = security_system.create_token(user_id)
    return JSONResponse({"token": token, "user_id": user_id})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
