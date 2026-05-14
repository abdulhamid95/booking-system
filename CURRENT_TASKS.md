# CURRENT_TASKS.md

> هذا الملف يحتوي فقط على المهام النشطة حالياً.  
> بقية المهام موجودة في [BACKLOG.md](BACKLOG.md) وستُضاف هنا عند حلول دورها.  
> المهام المنجزة تُنقل إلى [DONE.md](DONE.md) بموافقة مدير المشروع.

---

## ملخص المهام النشطة

| المهمة | العنوان | الـ Epic | الحالة |
|--------|---------|---------|--------|
| TASK-012 | إنشاء نموذج الحجز Booking | EPIC-06 | 🔄 نشطة |
| TASK-013 | منع تداخل الحجوزات | EPIC-06 | ⏳ معلقة |

---

## EPIC-06 — نظام الحجوزات

### TASK-012: إنشاء نموذج الحجز Booking

**الأولوية:** P1  
**النوع:** Backend  
**الحالة:** 🔄 نشطة

**الوصف:**  
إنشاء نموذج Django يمثل حجز العميل داخل تطبيق `bookings`.

**الحقول المطلوبة:**
- `business` — ForeignKey → Business
- `service` — ForeignKey → Service
- `staff_member` — ForeignKey → StaffMember
- `customer_name` — CharField
- `customer_phone` — CharField
- `customer_email` — EmailField (اختياري)
- `start_time` — DateTimeField
- `end_time` — DateTimeField
- `status` — CharField (choices: pending / confirmed / cancelled)
- `notes` — TextField (اختياري)
- `created_at` — DateTimeField (auto)

**حالات الحجز:**
- `pending` — بانتظار التأكيد
- `confirmed` — مؤكد (الافتراضي في MVP)
- `cancelled` — ملغى

**معايير القبول:**
- كل حجز مرتبط بمنشأة وخدمة وموظف.
- يتم حساب `end_time` بناءً على `start_time` ومدة الخدمة (`duration_minutes`).
- الحالة الافتراضية للحجز هي `confirmed`.

---

### TASK-013: منع تداخل الحجوزات

**الأولوية:** P1  
**النوع:** Backend / Business Logic  
**الحالة:** ⏳ معلقة — تبدأ بعد TASK-012

**الوصف:**  
منع إنشاء حجزين لنفس الموظف في نفس الوقت.

**القاعدة الأساسية:**  
لا يمكن إنشاء حجز جديد إذا كان هناك حجز آخر لنفس الموظف يتداخل معه زمنيًا.

**مثال:**  
إذا كان لدى الموظف حجز من 10:00 إلى 10:30، فلا يمكن إنشاء حجز آخر يبدأ في 10:15.

**معايير القبول:**
- النظام يرفض الحجز المتداخل.
- التحقق يتم في backend (model أو serializer) وليس فقط في الواجهة.
- الحجوزات الملغاة (`cancelled`) لا تمنع حجز موعد جديد.

---

> **EPIC-01** ✅ مكتمل — **EPIC-02** ✅ مكتمل — **EPIC-03** ✅ مكتمل  
> **EPIC-04** ✅ مكتمل — **EPIC-05** ✅ مكتمل  
> **EPIC-06** 🔄 قيد التنفيذ — التالي: **EPIC-07 — واجهات الحجز العامة** (TASK-014, TASK-015)
