# VipraTech Store - Stripe Payment Assignment

A production-ready Django application featuring Stripe test payments with comprehensive protection against double charges and refresh-safe payment confirmation.

🎉 **Now Live in Production!** Deployed on Render with PostgreSQL from Neon DB

---

## 🚀 Live Demo & Quick Access

### **Production Links**
- 🏪 **Store**: [https://vipratech-assignment-test.onrender.com](https://vipratech-assignment-test.onrender.com)
- 🔐 **Admin Panel**: [https://vipratech-assignment-test.onrender.com/admin](https://vipratech-assignment-test.onrender.com/admin)
  - **Username**: `vipratech`
  - **Password**: `1234`

### **Docker Image**
```bash
docker pull saurabh1244/vipratech-assignment-test:latest
```

### **Quick Start** (Choose one):

#### **Option 1: Run Locally from Docker Image** ⚡ (Easiest)
```bash
docker pull saurabh1244/vipratech-assignment-test:latest
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY \
  -e STRIPE_SECRET_KEY=sk_test_YOUR_KEY \
  -e DB_NAME=vipra_db \
  -e DB_USER=vipra_user \
  -e DB_PASSWORD=vipra_password \
  -e DB_HOST=your_neon_host \
  -e DB_PORT=5432 \
  saurabh1244/vipratech-assignment-test:latest
```

#### **Option 2: Run with Docker Compose** (Full Setup)
```bash
git clone https://github.com/yourusername/vipratech-assignment-test.git
cd vipratech-assignment-test
cp .env.example .env
# Edit .env with your credentials
docker-compose up --build
```

#### **Option 3: Run Locally with Python** (Development)
```bash
git clone https://github.com/yourusername/vipratech-assignment-test.git
cd vipratech-assignment-test
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database and Stripe credentials
python manage.py migrate
python manage.py runserver
```

---

## 📋 Assignment Overview

**Duration**: 48 Hours | **Framework**: Django 5.2 + PostgreSQL | **Payment**: Stripe (Test Mode)

**Deployment**: Production-ready on Render | **Database**: Neon DB (Serverless PostgreSQL)

**Core Requirements**:
- ✅ Django application with one HTML page displaying three fixed products
- ✅ User quantity input and "Buy" functionality
- ✅ Stripe test mode payment processing
- ✅ Paid orders visible after successful payment on the same page
- ✅ Protection against double charges and refresh issues
- ✅ User authentication system
- ✅ Bootstrap-based responsive styling (Tailwind CSS)
- ✅ Dockerized setup for production deployment

---

## 🎯 Key Design Decisions

### 1. **Stripe Flow: Checkout Sessions**

**Choice**: Stripe Checkout Sessions (`mode="payment"`)

**Reasoning**:
- ✅ **Built-in PCI Compliance**: Stripe hosts the checkout page—no need to handle card data
- ✅ **Idempotency**: Session IDs are unique per order, preventing duplicate charges on retries
- ✅ **User Experience**: Seamless redirect to Stripe-hosted form, then back to success URL
- ✅ **Mobile Optimized**: Automatically responsive across all devices
- ✅ **Fewer Integration Headaches**: No manual webhook parsing required for basic flows

**Alternative Considered**: Payment Intents API would require:
- Handling card tokenization on frontend (higher PCI responsibility)
- Manual confirmation flow with client secret
- More complex webhook management

---

## 🔐 Double-Charge Prevention Strategy

### **Multi-Layer Protection**:

1. **Database-Level Uniqueness Constraint**
   - `stripe_session_id` field is `unique=True` in Order model
   - Prevents duplicate Order records even if checkout endpoint is called twice

2. **Order Status Check Before Payment Verification**
   ```python
   if order.status == Order.Status.PENDING:
       # Only verify and update if PENDING
       session = stripe.checkout.Session.retrieve(session_id)
       if session.payment_status == "paid":
           order.status = Order.Status.PAID
           order.save()
   ```
   - If order is already PAID, subsequent requests simply display success message
   - Status is immutable once marked as PAID

3. **Idempotent Success URL Handling**
   - Success URL returns `?session_id={CHECKOUT_SESSION_ID}`
   - Same session ID in URL always maps to same order in database
   - Users can refresh page without creating duplicate charges

4. **Stripe Session Retrieval (No Duplicate Billing)**
   - Stripe API call only *verifies* payment status
   - Does NOT charge the customer again
   - Stripe guarantees one payment per session

5. **Transaction-Safe Cleanup**
   - Only cancel order on checkout creation exception
   - Never delete orders; use status states for audit trail

---

## 🏗️ Data Model Architecture

### **Product Model** (Immutable Catalog)
- Fixed products loaded via Django admin or initial migration
- `price_in_inr`: Stored in paise (lowest unit) to avoid float rounding issues
- `is_active`: Soft delete pattern for product catalog management

### **Order Model** (Payment Lifecycle)
- **Status States**: PENDING → PAID | CANCELED
- `user`: ForeignKey to User (nullable for guest checkouts in future)
- `stripe_session_id`: Unique identifier linking to Stripe
- `stripe_payment_intent_id`: Stored for future refund/dispute handling

### **OrderItem Model** (Cart Snapshot)
- Stores unit price at purchase time (handles price changes)
- `product`: ForeignKey to Product (PROTECT to prevent deletion of sold items)
- Quantity and unit price immutable after order creation

**Why This Design**:
- ✅ Audit trail: Never delete orders
- ✅ Extensibility: Can add refunds, cancellations, shipping
- ✅ Price history: OrderItem stores price independent of Product changes

---

## 📝 Assumptions Made

1. **Single Currency**: All prices in INR (Indian Rupees); amounts stored in paise (lowest unit)
2. **No Inventory**: Products are unlimited (no stock tracking)
3. **No Guest Checkout**: Cart associated with authenticated users only (can extend with sessions)
4. **One Stripe Account**: Single secret key for all payments
5. **Success URL Redirect**: Post-payment redirect happens immediately (not webhook-based)
6. **No Subscriptions**: One-time payments only; Stripe mode="payment"
7. **No Refunds UI**: Refunds handled in Django admin via Stripe dashboard
8. **No Tax Calculation**: Prices displayed as-is; can extend with tax rates


---
## 🚀 Setup Instructions

### **Prerequisites**
- Python 3.11+
- Docker & Docker Compose (for containerized setup)
- PostgreSQL 15 (Local, Docker, or Neon DB)
- Stripe Test Account (free at [stripe.com](https://stripe.com))
- Neon DB Account (free at [neon.tech](https://neon.tech)) - **Recommended for Production**

### **Local Development Setup**

1. **Clone and Navigate**
   ```bash
   cd d:\VipraTest2
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy example to .env
   copy .env.example .env  # Windows
   # or
   cp .env.example .env    # macOS/Linux
   ```

5. **Edit `.env` with Your Credentials** (Three Options)

   **Option A: Local PostgreSQL**
   ```env
   DJANGO_SECRET_KEY=your-super-secret-key-change-this
   DEBUG=1
   
   DB_NAME=vipra_db
   DB_USER=vipra_user
   DB_PASSWORD=vipra_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_SSL=0
   
   STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
   
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   **Option B: Neon DB (Cloud PostgreSQL)** ⭐ *Recommended for Production*
   ```env
   DJANGO_SECRET_KEY=your-super-secret-key-change-this
   DEBUG=0  # Set to 0 in production
   
   # Get these from Neon Console → Project → Connection String
   DB_NAME=your_db_name
   DB_USER=your_neon_user
   DB_PASSWORD=your_neon_password
   DB_HOST=ep-your-project.neon.tech  # Neon endpoint
   DB_PORT=5432
   DB_SSL=1  # Neon requires SSL
   
   STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
   
   ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
   ```

   **Option C: Docker Postgres**
   ```env
   DJANGO_SECRET_KEY=your-super-secret-key-change-this
   DEBUG=1
   
   DB_NAME=vipra_db
   DB_USER=vipra_user
   DB_PASSWORD=vipra_password
   DB_HOST=db  # Docker service name
   DB_PORT=5432
   DB_SSL=0
   
   STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
   
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   **Get Stripe Keys**:
   - Go to [Stripe Dashboard](https://dashboard.stripe.com) → Developers → API Keys
   - Copy Publishable and Secret keys (test mode)

6. **Setup PostgreSQL** (Option A: Local)
   ```bash
   # Ensure PostgreSQL 15 is running locally
   # Create database and user with credentials from .env
   ```

   **Option B: Use Docker for Database Only**
   ```bash
   docker run -d \
     --name vipra_postgres \
     -e POSTGRES_DB=vipra_db \
     -e POSTGRES_USER=vipra_user \
     -e POSTGRES_PASSWORD=vipra_password \
     -p 5432:5432 \
     postgres:15
   ```

7. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

8. **Create Superuser** (Optional, for Django Admin)
   ```bash
   python manage.py createsuperuser
   ```

9. **Load Sample Products** (Via Django Shell)
   ```bash
   python manage.py shell
   ```
   ```python
   from store.models import Product
   
   Product.objects.create(
       name="Premium Pro Subscription",
       description="Advanced features + priority support",
       price_in_inr=49999,  # ₹499.99
       is_active=True
   )
   Product.objects.create(
       name="Basic Package",
       description="Core features for individuals",
       price_in_inr=9999,   # ₹99.99
       is_active=True
   )
   Product.objects.create(
       name="Enterprise License",
       description="Full suite + dedicated account manager",
       price_in_inr=499999,  # ₹4,999.99
       is_active=True
   )
   exit()
   ```

10. **Run Development Server**
    ```bash
    python manage.py runserver
    ```

11. **Access Application**
    - **Store**: http://localhost:8000
    - **Admin**: http://localhost:8000/admin

---

### **Docker Compose Setup** (Recommended for CI/CD)

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Run Migrations Inside Container**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

3. **Access Application**
   - **Store**: http://localhost:8000
   - **Admin**: http://localhost:8000/admin

4. **Stop Services**
   ```bash
   docker-compose down
   ```

---

## 🌐 Production Deployment (Render + Neon DB)

### **Current Production Setup**
- **Host**: Render (render.com)
- **Database**: Neon DB (serverless PostgreSQL)
- **Docker Registry**: Docker Hub
- **Status**: ✅ Live and Running

### **Live Environment Configuration**

#### **Environment Variables Used in Production**
```env
# Django
DJANGO_SECRET_KEY=<production-secret-key>
DEBUG=0
ALLOWED_HOSTS=vipratech-assignment-test.onrender.com
CSRF_TRUSTED_ORIGINS=https://vipratech-assignment-test.onrender.com

# Database (Neon DB)
DB_ENGINE=postgresql
DB_NAME=neon_db_name
DB_USER=neon_user
DB_PASSWORD=<neon-password>
DB_HOST=ep-<your-neon-host>.neon.tech
DB_PORT=5432
DB_SSL=1

# Stripe (Test Mode)
STRIPE_PUBLISHABLE_KEY=pk_test_<your-key>
STRIPE_SECRET_KEY=sk_test_<your-key>
```

### **How to Deploy Your Own Instance to Render**

#### **Step 1: Prepare Docker Image**
```bash
# Build and push to Docker Hub
docker build -t yourusername/vipratech-assignment-test:latest .
docker push yourusername/vipratech-assignment-test:latest
```

#### **Step 2: Setup Neon DB**
1. Go to [Neon Console](https://console.neon.tech)
2. Create new project (PostgreSQL 15)
3. Copy connection string from Dashboard
4. Note: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

#### **Step 3: Deploy on Render**
1. Visit [render.com](https://render.com)
2. Create new **Web Service**
3. Select **Docker** as runtime
4. Provide Docker image: `yourusername/vipratech-assignment-test:latest`
5. Add environment variables from section above
6. Set Port: `8000`
7. Deploy!

#### **Step 4: Verify Deployment**
```bash
# Check application
curl https://your-app-name.onrender.com

# Check admin
curl https://your-app-name.onrender.com/admin

# View logs
# Use Render dashboard → Logs tab
```

### **Production Checklist**
- [x] Django settings: `DEBUG=False`
- [x] Database: Neon DB (serverless, no maintenance)
- [x] Static files: Served via WhiteNoise
- [x] Stripe: Test mode (change to live when needed)
- [x] HTTPS: Enabled by default on Render
- [x] CSRF: Configured for production domain
- [x] Admin: Accessible at `/admin` with credentials

---

## 💳 Testing Stripe Payments

### **Try the Live Demo** 🎯
Visit: [https://vipratech-assignment-test.onrender.com](https://vipratech-assignment-test.onrender.com)

Or test locally by following setup instructions above.

### **Test Card Numbers** (Stripe Provided)
| Card Number | Scenario |
|---|---|
| `4242 4242 4242 4242` | ✅ Successful payment |
| `4000 0000 0000 0002` | ❌ Card declined |
| `4000 0025 0000 3155` | 🔐 Requires 3D Secure |

- **Expiry**: Any future date (e.g., `12/25`)
- **CVC**: Any 3 digits (e.g., `123`)

### **Payment Flow Steps**
1. **Register / Login** - Create account or use existing credentials
2. **Add Products** - Enter quantities for products (1, 2, or 3)
3. **Proceed to Checkout** - Click "Buy Now" button
4. **Enter Card Details** - Use test card `4242 4242 4242 4242`
5. **Complete Payment** - Click Pay button
6. **Success Confirmation** - Redirected to home with "Payment successful!" message
7. **View Order** - "My Orders" section shows your paid order (must be logged in)

### **Verify Double-Charge Prevention** ✅
1. ✅ Complete a payment successfully
2. ✅ Refresh page → Should show success message WITHOUT re-charging
3. ✅ Hit browser back button → Success persists, no duplicate order
4. ✅ Check admin panel → Only ONE order created (not duplicated)

### **Test Admin Panel**
- **URL**: [https://vipratech-assignment-test.onrender.com/admin](https://vipratech-assignment-test.onrender.com/admin)
- **Username**: `vipratech`
- **Password**: `1234`
- **Features**: View orders, products, users, manage inventory

---

## 📁 Project Structure

```
d:\VipraTest2/
├── store/                          # Django App
│   ├── models.py                   # Product, Order, OrderItem
│   ├── views.py                    # store_home, create_checkout, register_view
│   ├── urls.py                     # URL routing
│   ├── admin.py                    # Django Admin registration
│   ├── migrations/                 # Database schema
│   └── templates/store/
│       ├── index.html              # Main store page (products + orders)
│       ├── login.html              # Login form
│       └── register.html           # User registration form
├── vipratest/                      # Django Project Config
│   ├── settings.py                 # Django settings (DB, Stripe, Auth)
│   ├── urls.py                     # Main URL routing
│   ├── wsgi.py                     # WSGI app for Gunicorn
│   └── asgi.py                     # ASGI app (async support)
├── staticfiles/                    # Compiled static assets
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
├── docker-compose.yml              # Multi-container orchestration
├── manage.py                       # Django CLI
├── .env.example                    # Environment template
├── README.md                       # This file
└── AI-ASSIST.md                    # AI tool usage documentation
```

---

## 🛠️ Technology Stack

| Component | Choice | Version | Rationale |
|---|---|---|---|
| **Framework** | Django | 5.2.10 | Latest LTS; security-focused |
| **Database** | PostgreSQL | 15 | Production-grade ACID compliance |
| **Cloud Database** | Neon DB | Latest | Serverless PostgreSQL (no maintenance) |
| **Hosting** | Render | Latest | Simple Docker deployment, auto-scaling |
| **Container Registry** | Docker Hub | Latest | Public image repository |
| **Payment** | Stripe | 14.2.0 (API v1) | PCI-compliant, no card handling |
| **Frontend** | Tailwind CSS | Latest | Utility-first, responsive design |
| **Admin UI** | Django Jazzmin | 3.0.1 | Modern admin interface |
| **Web Server** | Gunicorn | 24.1.1 | WSGI app server for production |
| **Static Files** | WhiteNoise | 6.11.0 | Efficient static file serving |
| **Containerization** | Docker + Compose | Latest | Reproducible deployments |

**Production Environment**:
- Render (render.com) - Hosting
- Neon DB (neon.tech) - Database
- Docker Hub - Image Registry
- Stripe Test Mode - Payment Processing

---

## 📊 Key Features Implemented

✅ **User Authentication**
- Registration with username/password
- Login/logout functionality
- Order history visible only to authenticated users

✅ **Product Management**
- Three fixed products in database
- Admin interface for adding more products
- Soft delete (is_active field) for legacy support

✅ **Payment Processing**
- Stripe Checkout Sessions (PCI-compliant)
- Real-time payment status verification
- Order status tracking (PENDING → PAID → CANCELED)

✅ **Refresh-Safe Confirmation**
- Success URL includes session_id parameter
- Payment verified from Stripe session (not repeated)
- Messages persist across page reloads

✅ **Order History**
- "My Orders" section for authenticated users
- Orders paginated by creation date (newest first)
- Shows order items with quantities and prices

✅ **Error Handling**
- Graceful fallbacks if Stripe API unavailable
- User-friendly error messages for payment failures
- Validation for product quantities

✅ **Production Readiness**
- Docker containerization
- Environment variable configuration
- PostgreSQL for data durability
- CSRF protection and secure headers
- Whitenoise for static file compression

---

## 🧪 Code Quality & Testing

### **Testing Manual Checklist**
- [ ] Register new account
- [ ] Login with valid credentials
- [ ] Add quantities to products
- [ ] Complete Stripe test payment (4242 4242 4242 4242)
- [ ] Verify order appears in "My Orders"
- [ ] Refresh page → No duplicate orders
- [ ] Test with declined card (4000 0000 0000 0002)
- [ ] Logout and verify paid orders hidden
- [ ] Test Docker build and deployment

### **Code Standards**
- **Type Hints**: Used in models and functions for clarity
- **Docstrings**: Added to complex functions
- **DRY Principle**: Reusable utilities for Stripe operations
- **Security**: No hardcoded secrets; environment variables only
- **Logging**: Django debug messages for errors and success states

### **Performance Considerations**
- **Database**: `prefetch_related()` for OrderItem queries (N+1 prevention)
- **Stripe**: Session retrieval cached in Order model
- **Caching**: WhiteNoise compresses static assets
- **Async**: ASGI configured for future WebSocket support






---

## 🐛 Known Limitations

1. **No Webhook Confirmation**: Relies on redirect-based verification (acceptable for low-volume)
2. **Cart Persistence**: Quantities only during checkout session
3. **No Rate Limiting**: Could add Django-Ratelimit for brute force protection
4. **Admin Only**: No customer-facing refund requests (future enhancement)

---

## 📚 References

- [Stripe Checkout Documentation](https://stripe.com/docs/checkout)
- [Django Official Docs](https://docs.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 🤝 Responsible AI Usage

This project was developed using AI-assisted tools for:
- Tailwind CSS UI improvements and layout ideas
- Error debugging and resolution
- Documentation generation
- Stripe integration best practices research
- Docker + PostgreSQL setup structure
- Double-charge / refresh-safe strategy recommendations


**See [AI-ASSIST.md](AI-ASSIST.md) for detailed tool usage and where each tool was applied.**

**Transparency Note**: All code was reviewed and understood by the developer. No secrets or credentials were exposed to AI. Core payment logic was manually verified against Stripe documentation.

---

## ⏱️ Development Time

- **Total Time Spent**: ~8-10 hours
  - Planning & Design: 1.5 hours
  - Model & View Implementation: 1 hours
  - Template & Frontend: 1 hours
  - Stripe Integration & Testing: 30 mins
  - Docker Setup & Deployment: 3 hour
  - Documentation: 1 hours

---

## 📄 License

This project is provided as-is for educational and assignment purposes.

---

## ✉️ Support & Resources

### **Live Demo**
- 🏪 **Store**: https://vipratech-assignment-test.onrender.com
- 🔐 **Admin**: https://vipratech-assignment-test.onrender.com/admin (vipratech / 1234)

### **Docker Image**
- 🐳 **Registry**: Docker Hub
- 📦 **Image**: `saurabh1244/vipratech-assignment-test:latest`
- 📥 **Pull**: `docker pull saurabh1244/vipratech-assignment-test:latest`

### **Troubleshooting**

| Issue | Solution |
|---|---|
| **Can't connect to database** | Check `DB_HOST`, `DB_PORT`, `DB_PASSWORD` in `.env` |
| **Stripe not working** | Verify `STRIPE_SECRET_KEY` is correct (sk_test_...) |
| **Migrations failed** | Run `python manage.py migrate` after DB is ready |
| **Admin login fails** | Use `vipratech` / `1234` or create new user with `createsuperuser` |
| **Static files not loading** | Run `python manage.py collectstatic --noinput` |
| **Docker image won't pull** | Check Docker is installed: `docker --version` |

### **Getting Help**
1. Check `.env.example` for required configuration
2. Review Stripe test card numbers above
3. Ensure PostgreSQL (local or Neon) is running
4. Run migrations: `python manage.py migrate`
5. Check application logs: `python manage.py runserver` (local) or Render dashboard (production)

---

## 📊 Project Summary

| Aspect | Details |
|---|---|
| **Live URL** | https://vipratech-assignment-test.onrender.com |
| **Admin Panel** | https://vipratech-assignment-test.onrender.com/admin |
| **Docker Image** | saurabh1244/vipratech-assignment-test:latest |
| **Database** | Neon DB (PostgreSQL 15) |
| **Hosting** | Render |
| **Payment** | Stripe Test Mode |
| **Admin User** | vipratech / 1234 |
| **Status** | ✅ Production Ready |

---

**Last Updated**: January 29, 2026  
**Django Version**: 5.2.10  
**Stripe API**: v1 (14.2.0)  
**Deployment**: Render + Neon DB + Docker Hub  
**Status**: 🟢 Live & Running
