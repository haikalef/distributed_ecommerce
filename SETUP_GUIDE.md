# 🚀 Distributed E-Commerce Order System - Setup Guide

## 📌 Overview

Panduan lengkap untuk menjalankan project Distributed E-Commerce Order System dengan Docker Compose. Project ini sudah dioptimalkan untuk menghindari port conflict dengan aplikasi lain di device Anda.

---

## ⚙️ Konfigurasi Port (PENTING!)

### Port Mapping Explanation

```
External (Host) Port ➜ Internal (Container) Port

📦 MySQL Database:
   3307 ➜ 3306
   (Host access: localhost:3307, Container: mysql:3306)

🔴 Redis Cache:
   6379 ➜ 6379
   (Standard Redis port, no conflict)

🌐 FastAPI Web Server:
   8000 ➜ 8000
   (Host access: http://localhost:8000)

🔄 Celery Worker:
   (Background service, no external port)
```

**Key Point:** MySQL external port diubah dari 3306 menjadi 3307 untuk menghindari conflict dengan MySQL service yang sudah berjalan di host machine Anda.

---

## 🏁 Step-by-Step Setup

### Step 1: Pastikan Docker Desktop Running

```bash
# Windows
1. Buka "Docker Desktop" dari Start Menu
2. Tunggu status berubah menjadi "Running"
3. Verifikasi di PowerShell:
   docker --version
   # Expected: Docker version XX.XX.XX, ...
```

### Step 2: Clone Repository

```bash
# Buka PowerShell/Terminal di folder tempat Anda ingin project
cd C:\Users\YourName\Documents  # Contoh Windows

# Clone repository
git clone https://github.com/haikalef/distributed_ecommerce.git
cd distributed_ecommerce
```

### Step 3: Clean Up Old Docker Resources (PENTING!)

Jika Anda sebelumnya menjalankan project dan error port conflict:

```bash
# Stop all containers
docker-compose down

# Remove old containers dan volumes
docker-compose down -v

# Verify no old containers running
docker ps -a | grep distributed
```

### Step 4: Build dan Run dengan Docker Compose

```bash
# Di folder distributed_ecommerce
# Build images dan jalankan semua services (JANGAN SKIP!)
docker-compose up -d

# Tunggu 30-60 detik untuk semua services siap
```

**Expected output:**
```
✔ Network distributed-ecommerce_ecommerce_network  Created
✔ Volume distributed-ecommerce_mysql_data          Created
✔ Volume distributed-ecommerce_redis_data          Created
✔ Container distributed_ecommerce_mysql            Started
✔ Container distributed_ecommerce_redis            Started
✔ Container distributed_ecommerce_web              Started
✔ Container distributed_ecommerce_celery_worker    Started
```

### Step 5: Verifikasi Semua Services Running

```bash
# Check status semua container
docker-compose ps

# Expected output:
NAME                                  STATUS           PORTS
distributed_ecommerce_mysql           Up (healthy)     0.0.0.0:3307->3306/tcp
distributed_ecommerce_redis           Up (healthy)     0.0.0.0:6379->6379/tcp
distributed_ecommerce_web             Up               0.0.0.0:8000->8000/tcp
distributed_ecommerce_celery_worker   Up               -
```

✅ **Jika semua "Up" - Anda sudah berhasil!**

---

## 🌐 Akses Aplikasi

### FastAPI API Documentation

```
Buka di browser: http://localhost:8000/docs

Atau: http://localhost:8000/redoc (alternative format)
```

### API Endpoints

Semua endpoint sudah tersedia di Swagger UI untuk testing interaktif.

---

## 🧪 Quick Testing

### Test 1: Create Product

**Di Swagger UI atau Terminal:**

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 16",
    "price": 12000000,
    "stock": 10
  }'

# Expected Response (201 Created):
# {"id": 1, "name": "iPhone 16", "price": 12000000, "stock": 10}
```

### Test 2: Get All Products

```bash
curl http://localhost:8000/products

# Expected Response (200 OK):
# [{"id": 1, "name": "iPhone 16", "price": 12000000, "stock": 10}]
```

### Test 3: Create Order

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# Expected Response (201 Created):
# {"id": 1, "product_id": 1, "quantity": 2, "created_at": "2026-01-09T..."}

# Note: Celery task automatically triggered (async processing)
```

### Test 4: Verify Stock Decreased

```bash
curl http://localhost:8000/products/1

# Expected Response:
# {"id": 1, "name": "iPhone 16", "price": 12000000, "stock": 8}
# Stock turun dari 10 menjadi 8 ✅
```

---

## 📊 Monitoring & Debugging

### View Logs Real-Time

```bash
# Semua logs dari semua services
docker-compose logs -f

# Logs dari specific service
docker-compose logs -f web            # FastAPI
docker-compose logs -f celery_worker  # Celery tasks
docker-compose logs -f mysql          # Database
docker-compose logs -f redis          # Cache
```

### Check Service Health

```bash
# MySQL health check
docker-compose exec mysql mysqladmin ping
# Expected: mysqld is alive

# Redis health check
docker-compose exec redis redis-cli ping
# Expected: PONG
```

### Access MySQL Database

```bash
# Login ke MySQL
docker-compose exec mysql mysql -u app_user -p distributed_ecommerce
# Password: app_password

# View tables
mysql> SHOW TABLES;
mysql> SELECT * FROM products;
mysql> SELECT * FROM orders;
```

### Check Redis Cache

```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# View all keys
> KEYS *

# Get specific key
> GET product:1

# Exit
> EXIT
```

---

## ❌ Troubleshooting

### Problem: "Port already in use"

**Solution:** Port 3307 atau 6379 atau 8000 masih terpakai

```bash
# Cek apa yang menggunakan port
netstat -ano | findstr :3307
netstat -ano | findstr :6379
netstat -ano | findstr :8000

# Kill process jika diperlukan
taskkill /PID [PID_NUMBER] /F

# Atau ubah port di docker-compose.yml
# ports:
#   - "3308:3306"  # Ganti 3307 menjadi 3308
```

### Problem: MySQL tidak bisa connect

```bash
# Check MySQL logs
docker-compose logs mysql

# Restart MySQL
docker-compose restart mysql

# Full reset
docker-compose down -v
docker-compose up -d
```

### Problem: Celery worker tidak processing

```bash
# Check Celery logs
docker-compose logs celery_worker

# Verify Redis is running
docker-compose exec redis redis-cli ping

# Restart worker
docker-compose restart celery_worker
```

### Problem: Web service error saat startup

```bash
# Check web logs
docker-compose logs web

# Rebuild image
docker-compose down
docker-compose up -d --build
```

---

## 🛑 Cara Berhenti Services

```bash
# Stop semua services (data tetap)
docker-compose down

# Stop dan hapus semua data (fresh restart)
docker-compose down -v

# Restart services
docker-compose up -d
```

---

## 📈 Performance Testing - Race Condition

```bash
# Terminal 1: Monitor logs
docker-compose logs -f web

# Terminal 2: Create product dengan limited stock
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Limited", "price": 100000, "stock": 1}'

# Terminal 3: 5 concurrent orders (only 1 should succeed)
for i in {1..5}; do
  curl -X POST http://localhost:8000/orders \
    -H "Content-Type: application/json" \
    -d '{"product_id": 2, "quantity": 1}' &
done
wait

# Terminal 2: Verify only 1 succeeded
curl http://localhost:8000/orders
```

**Expected Result:** Hanya 1 order dengan status 201, 4 orders error 400 (Insufficient stock) ✅

---

## 📝 Summary

| Task | Status | Port |
|------|--------|------|
| FastAPI Web | ✅ Running | 8000 |
| MySQL Database | ✅ Running | 3307 (ext) → 3306 (int) |
| Redis Cache | ✅ Running | 6379 |
| Celery Worker | ✅ Running | - |
| API Docs | ✅ Available | /docs |
| Race Condition Handling | ✅ Implemented | - |
| Background Tasks | ✅ Implemented | - |

---

## 🆘 Need Help?

1. **Check logs:** `docker-compose logs -f`
2. **Check README.md** untuk dokumentasi lengkap
3. **Verify ports:** `netstat -ano | findstr :PORT`
4. **Reset everything:** `docker-compose down -v && docker-compose up -d`

---

## ✅ Checklist Sebelum Submisi

- [ ] Docker Desktop running
- [ ] `docker-compose up -d` berhasil
- [ ] Semua container "Up"
- [ ] API accessible di http://localhost:8000/docs
- [ ] Product CRUD berfungsi
- [ ] Order creation berfungsi
- [ ] Celery task terproses (lihat logs)
- [ ] Race condition handling tested
- [ ] Database data persisted

---

**Selamat! Anda sudah siap menjalankan Distributed E-Commerce Order System! 🎉**
