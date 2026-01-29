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

## 🎯 Stripe Flow Choice & Reasoning

### **Chosen: Stripe Checkout Sessions**

**Choice**: Stripe Checkout Sessions (`mode="payment"`)

**Why This Approach**:
- ✅ **Built-in PCI Compliance**: Stripe hosts the checkout page—no need to handle card data
- ✅ **Idempotency**: Session IDs are unique per order, preventing duplicate charges on retries
- ✅ **User Experience**: Seamless redirect to Stripe-hosted form, then back to success URL
- ✅ **Mobile Optimized**: Automatically responsive across all devices
- ✅ **Fewer Integration Headaches**: No manual webhook parsing required for basic flows

**Alternative Rejected**: Payment Intents API
- Higher PCI responsibility (manual card tokenization)
- More complex client secret flow
- Requires webhook management for async confirmation

**Technical Implementation**:
- Orders created with `status=PENDING` before redirect
- Stripe session ID stored in database
- Post-payment: Session retrieved and verified
- Status updated to `PAID` only after verification

---

## 🔐 Double-Charge Prevention Strategy

### **Multi-Layer Protection**:

1. **Database-Level Uniqueness Constraint**
   - `stripe_session_id` field is `unique=True` in Order model
   - Prevents duplicate Order records even if checkout endpoint called twice

2. **Order Status Check Before Verification**
   ```python
   if order.status == Order.Status.PENDING:
       session = stripe.checkout.Session.retrieve(session_id)
       if session.payment_status == "paid":
           order.status = Order.Status.PAID
           order.save()
   ```
   - Only PENDING orders verified once
   - Status immutable after PAID

3. **Idempotent Success URL**
   - Success URL: `?session_id={CHECKOUT_SESSION_ID}`
   - Same session ID = same order (no duplicates)
   - Refresh-safe (no re-billing)

4. **Stripe Session Guarantee**
   - Session retrieval only *verifies* payment
   - Does NOT charge customer again
   - One payment per session guaranteed

5. **Transaction-Safe Cleanup**
   - Only cancel on checkout creation exception
   - Never delete orders (audit trail preserved)

---



## 📋 .env Configuration

### **Required Environment Variables**

```env
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=1  # Set to 0 for production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Choose one option below)
# Option A: Local PostgreSQL
DB_NAME=vipra_db
DB_USER=vipra_user
DB_PASSWORD=vipra_password
DB_HOST=localhost
DB_PORT=5432
DB_SSL=0

# Option B: Neon DB (Cloud PostgreSQL) - Recommended for Production
# DB_HOST=ep-your-project.neon.tech
# DB_SSL=1

# Stripe Test Keys (from dashboard.stripe.com)
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
```

### **Get Stripe Keys**
1. Go to [Stripe Dashboard](https://dashboard.stripe.com) → Developers → API Keys
2. Copy test mode Publishable and Secret keys
3. Add to .env file

### **Using Docker Image**
```bash
docker pull saurabh1244/vipratech-assignment-test:latest
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_... \
  -e STRIPE_SECRET_KEY=sk_test_... \
  -e DB_HOST=your-db-host \
  saurabh1244/vipratech-assignment-test:latest
```

---

## 🧪 Notes on Code Quality

### **Code Standards**
- ✅ **Type Hints**: Used in models and functions for clarity
- ✅ **DRY Principle**: Reusable utilities for Stripe operations
- ✅ **Security**: No hardcoded secrets; environment variables only
- ✅ **Error Handling**: Graceful fallbacks if Stripe API unavailable
- ✅ **Database Optimization**: `prefetch_related()` for OrderItem queries (N+1 prevention)

### **Testing Checklist**
- [ ] Register new account
- [ ] Login with valid credentials  
- [ ] Add quantities to products
- [ ] Complete Stripe test payment (4242 4242 4242 4242)
- [ ] Verify order appears in "My Orders"
- [ ] Refresh page → No duplicate orders
- [ ] Test with declined card (4000 0000 0000 0002)
- [ ] Admin panel access


---









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

## ⏱️ Development Time

- **Total Time Spent**: ~6-8 hours
  - Planning & Design: 1.5 hours
  - Model & View Implementation: 1 hours
  - Template & Frontend: 1 hours
  - Stripe Integration & Testing: 30 mins
  - Docker Setup & Deployment: 3 hour
  - Documentation: 1 hours

---

## 🤝 Credits

See [AI-ASSIST.md](AI-ASSIST.md) for detailed tool usage in this project. All code was reviewed and understood by the developer.

