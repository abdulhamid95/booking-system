# دليل استخدام Mock Server — نظام إدارة الحجوزات

هذا الدليل موجّه لمطور الواجهة الأمامية (Frontend) الذي يبني واجهة المستخدم قبل اكتمال بيئة الـ Backend الحقيقية أو أثناء التطوير المتوازي.

---

## ما هو الـ Mock Server؟

الـ Mock Server هو خادم وهمي يستجيب بنفس شكل بيانات الـ API الحقيقي، لكن دون الحاجة إلى تشغيل Django أو قاعدة البيانات. يسمح لك ببناء الواجهة واختبارها بشكل مستقل.

---

## Base URL

```
https://bd3c81ad-2aac-46f8-bcdf-5d9e130183a4.mock.pstmn.io
```

استبدل هذا الرابط بـ `http://localhost:8000` عند التحول إلى البيئة الحقيقية.

---

## نقاط البداية السريعة (Quick Start)

```js
const MOCK_BASE = 'https://bd3c81ad-2aac-46f8-bcdf-5d9e130183a4.mock.pstmn.io';
const API_BASE  = 'http://localhost:8000'; // للبيئة الحقيقية

const BASE_URL = MOCK_BASE; // بدّل هذا السطر فقط عند الانتقال
```

---

## الـ Endpoints المتاحة

### أولاً — المسارات العامة (لا تحتاج Token)

هذه المسارات تُستخدم في صفحة الحجز العامة التي يراها العميل.

---

#### 1. جلب الخدمات المتاحة لمنشأة

```
GET /api/services/public/<business_id>/
```

**مثال:**
```
GET /api/services/public/1/
```

**الاستجابة (200):**
```json
[
  {
    "id": 1,
    "name": "قص شعر",
    "description": "قص شعر احترافي",
    "duration_minutes": 30,
    "price": "50.00"
  },
  {
    "id": 2,
    "name": "صبغة شعر",
    "description": null,
    "duration_minutes": 90,
    "price": "150.00"
  }
]
```

---

#### 2. جلب الموظفين المرتبطين بخدمة معينة

```
GET /api/staff/public/<business_id>/<service_id>/
```

**مثال:**
```
GET /api/staff/public/1/1/
```

**الاستجابة (200):**
```json
[
  {
    "id": 1,
    "name": "أحمد محمد",
    "photo": null
  },
  {
    "id": 2,
    "name": "سارة علي",
    "photo": null
  }
]
```

---

#### 3. جلب الأوقات المتاحة

```
GET /api/bookings/available-slots/?business_id=&service_id=&staff_id=&date=
```

**جميع البارامترات إلزامية.**

**مثال:**
```
GET /api/bookings/available-slots/?business_id=1&service_id=1&staff_id=1&date=2026-05-25
```

**الاستجابة (200):**
```json
{
  "date": "2026-05-25",
  "slots": [
    "09:00:00",
    "09:30:00",
    "10:00:00",
    "10:30:00",
    "11:00:00",
    "14:00:00",
    "14:30:00"
  ]
}
```

**ملاحظة:** ساعات العمل في الـ MVP هي 09:00–18:00. الأوقات المحجوزة مسبقًا لن تظهر.

**حالات الخطأ:**
```json
// 400 — بارامتر مفقود
{ "detail": "business_id, service_id, staff_id, and date are required." }

// 400 — تاريخ في الماضي
{ "date": "Date cannot be in the past." }

// 404 — خدمة غير موجودة
{ "service": "Service not found." }

// 404 — موظف غير مرتبط بالخدمة
{ "staff_member": "Staff member not found or does not provide this service." }
```

---

#### 4. إنشاء حجز جديد

```
POST /api/bookings/
Content-Type: application/json
```

**Body:**
```json
{
  "service": 1,
  "staff_member": 1,
  "date": "2026-05-25",
  "start_time": "10:00:00",
  "customer_name": "محمد عبدالله",
  "customer_phone": "0501234567",
  "customer_email": "customer@example.com",
  "notes": "أفضل الجانب الأيسر"
}
```

**الحقول الإلزامية:** `service`, `staff_member`, `date`, `start_time`, `customer_name`, `customer_phone`

**الحقول الاختيارية:** `customer_email`, `notes`

**الاستجابة (201):**
```json
{
  "reference_code": "BK-A3F9",
  "service_name": "قص شعر",
  "staff_name": "أحمد محمد",
  "date": "2026-05-25",
  "start_time": "10:00:00",
  "end_time": "10:30:00",
  "customer_name": "محمد عبدالله",
  "customer_phone": "0501234567",
  "status": "pending"
}
```

**حفظ الـ `reference_code` مهم** — يستخدمه العميل لتتبع حجزه لاحقًا.

---

### ثانيًا — المسارات المحمية (تحتاج Token)

هذه المسارات تُستخدم في لوحة تحكم صاحب المنشأة.

#### إرسال الـ Token في كل طلب محمي

```
Authorization: Token <your-token-here>
```

---

#### 5. تسجيل حساب صاحب منشأة جديد

```
POST /api/auth/register/business/
Content-Type: application/json
```

**Body:**
```json
{
  "username": "owner1",
  "email": "owner@example.com",
  "password": "StrongPass123",
  "business_name": "صالون النخبة",
  "business_phone": "0551234567",
  "business_address": "الرياض — حي النزهة"
}
```

**الاستجابة (201):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": { "id": 1, "username": "owner1", "email": "owner@example.com" },
  "business": { "id": 1, "name": "صالون النخبة", "phone": "0551234567" }
}
```

---

#### 6. تسجيل الدخول

```
POST /api/auth/login/
Content-Type: application/json
```

**Body:**
```json
{
  "username": "owner1",
  "password": "StrongPass123"
}
```

**الاستجابة (200):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": { "id": 1, "username": "owner1", "email": "owner@example.com" }
}
```

**احفظ الـ Token** في `localStorage` أو `sessionStorage`:
```js
localStorage.setItem('token', response.token);
```

---

#### 7. تسجيل الخروج

```
POST /api/auth/logout/
Authorization: Token <your-token>
```

**الاستجابة (204):** لا يوجد body.

---

#### 8. جلب/تعديل بيانات المستخدم الحالي

```
GET  /api/auth/me/
PATCH /api/auth/me/
Authorization: Token <your-token>
```

---

#### 9. إدارة الخدمات (لوحة التحكم)

| الطريقة | الـ Endpoint | الوصف |
|---------|------------|-------|
| GET | `/api/services/` | جلب كل الخدمات |
| POST | `/api/services/` | إنشاء خدمة جديدة |
| GET | `/api/services/<id>/` | جلب خدمة بعينها |
| PATCH | `/api/services/<id>/` | تعديل خدمة |
| POST | `/api/services/<id>/activate/` | تفعيل الخدمة |
| POST | `/api/services/<id>/deactivate/` | إيقاف الخدمة |

---

#### 10. إدارة الموظفين (لوحة التحكم)

| الطريقة | الـ Endpoint | الوصف |
|---------|------------|-------|
| GET | `/api/staff/` | جلب كل الموظفين |
| POST | `/api/staff/` | إضافة موظف |
| GET | `/api/staff/<id>/` | جلب موظف بعينه |
| PATCH | `/api/staff/<id>/` | تعديل موظف |
| POST | `/api/staff/<id>/activate/` | تفعيل الموظف |
| POST | `/api/staff/<id>/deactivate/` | إيقاف الموظف |

---

## مثال كامل — تدفق الحجز (JavaScript / Fetch)

```js
const BASE = 'https://bd3c81ad-2aac-46f8-bcdf-5d9e130183a4.mock.pstmn.io';

// الخطوة 1: جلب الخدمات
const services = await fetch(`${BASE}/api/services/public/1/`).then(r => r.json());

// الخطوة 2: جلب الموظفين للخدمة المختارة
const staff = await fetch(`${BASE}/api/staff/public/1/${services[0].id}/`).then(r => r.json());

// الخطوة 3: جلب الأوقات المتاحة
const slots = await fetch(
  `${BASE}/api/bookings/available-slots/?business_id=1&service_id=${services[0].id}&staff_id=${staff[0].id}&date=2026-05-25`
).then(r => r.json());

// الخطوة 4: إنشاء الحجز
const booking = await fetch(`${BASE}/api/bookings/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    service: services[0].id,
    staff_member: staff[0].id,
    date: '2026-05-25',
    start_time: slots.slots[0],
    customer_name: 'محمد عبدالله',
    customer_phone: '0501234567',
  }),
}).then(r => r.json());

console.log('رمز الحجز:', booking.reference_code);
```

---

## الانتقال من Mock إلى الـ API الحقيقي

عند جهوز بيئة الـ Backend الحقيقية:

1. بدّل `BASE_URL` من رابط الـ Mock إلى `http://localhost:8000`
2. تأكد من تشغيل Django: `python manage.py runserver`
3. توثيق Swagger متاح على: `http://localhost:8000/api/docs/`
4. توثيق Redoc متاح على: `http://localhost:8000/api/redoc/`

---

## روابط ذات صلة

- [معمارية النظام](ARCHITECTURE.md)
- [تصميم قاعدة البيانات](DATABASE_DESIGN.md)
- [وثيقة المتطلبات PRD](PRD.md)
