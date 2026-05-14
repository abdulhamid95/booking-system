# تصميم قاعدة البيانات - نظام إدارة الحجوزات

## الكيانات الأساسية

1. **Business** — المنشأة التي تستخدم النظام.
2. **User** — المستخدم الذي يملك حساب دخول (صاحب منشأة أو موظف).
3. **Staff** — الموظف أو مقدم الخدمة داخل المنشأة.
4. **StaffService** — جدول الربط بين الموظف والخدمات التي يقدّمها (M2M).
5. **Service** — الخدمة التي تقدمها المنشأة.
6. **WorkingHours** — أوقات العمل المتاحة لكل موظف.
7. **Customer** — العميل الذي يقوم بالحجز، مرتبط بالمنشأة.
8. **Booking** — عملية الحجز.
9. **Payment** — الدفعة المالية المرتبطة بالحجز.


## العلاقات الأساسية

- كل Business يملك عدة Users (عبر FK في User)
- كل Business يملك عدة Services
- كل Business يملك عدة Staff members
- كل Business يملك عدة Customers
- كل Staff ينتمي إلى Business واحدة
- كل Staff يرتبط بعدة Services عبر StaffService
- كل Staff يملك WorkingHours خاصة به (يوم واحد لكل سجل)
- كل Staff قد يرتبط اختيارياً بـ User واحد (لتمكين تسجيل الدخول)
- كل Booking يرتبط بـ Business واحدة، وService واحدة، وStaff واحد، وCustomer واحد
- كل Booking قد يملك Payment واحدة
- كل Customer يملك عدة Bookings


## الحقول الرئيسية

### Business
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| name | string | |
| type | string | صالون / عيادة / مدرب / مركز تجميل / مركز علاج |
| slug | string | فريد — يُستخدم في URL صفحة الحجز مثل `/book/salon-xyz` |
| email | string | فريد |
| phone | string | |
| address | string | |
| timezone | string | مثل `Asia/Riyadh` — افتراضي لكل أوقات المنشأة |
| is_active | boolean | للتحكم في تفعيل/تعطيل المنشأة |
| created_at | datetime | |
| updated_at | datetime | |


### User
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| business | FK → Business | ربط المستخدم بمنشأته |
| email | string | فريد |
| password | string | hashed |
| role | string | `owner` / `staff` — owner: صاحب المنشأة، staff: موظف بحساب دخول |
| is_active | boolean | |
| created_at | datetime | |
| updated_at | datetime | |


### Staff
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| business | FK → Business | |
| user | FK → User | اختياري — لتمكين الموظف من تسجيل الدخول ورؤية حجوزاته (US-08) |
| name | string | |
| email | string | |
| phone | string | |
| is_active | boolean | |
| created_at | datetime | |
| updated_at | datetime | |


### Service
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| business | FK → Business | |
| name | string | |
| description | string | اختياري |
| duration_minutes | integer | مدة الخدمة |
| buffer_time_minutes | integer | وقت الفاصل بعد الخدمة (تنظيف، راحة…) — افتراضي 0 |
| price | decimal | |
| is_active | boolean | |
| created_at | datetime | |
| updated_at | datetime | |


### StaffService
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| staff | FK → Staff | |
| service | FK → Service | |

> القيد: (staff, service) فريد — لا يتكرر نفس الربط.


### WorkingHours
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| staff | FK → Staff | |
| day_of_week | integer | 0=الأحد … 6=السبت |
| start_time | time | |
| end_time | time | |
| break_start | time | اختياري — بداية وقت الاستراحة |
| break_end | time | اختياري — نهاية وقت الاستراحة |
| is_active | boolean | يسمح بتعطيل يوم دون حذفه |

> القيد: (staff, day_of_week) فريد — يوم واحد لكل سجل لكل موظف.


### Customer
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| business | FK → Business | بيانات العملاء مُحاطة بنطاق كل منشأة |
| name | string | |
| phone | string | |
| email | string | |
| created_at | datetime | |

> القيد: (email, business) فريد — نفس البريد لا يُكرَّر داخل منشأة واحدة.


### Booking
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| business | FK → Business | |
| service | FK → Service | |
| staff | FK → Staff | |
| customer | FK → Customer | |
| booking_date | date | |
| start_time | time | |
| end_time | time | يُحسب تلقائياً: start_time + duration + buffer_time |
| status | string | `pending` / `confirmed` / `cancelled` / `completed` / `no_show` |
| notes | string | اختياري — ملاحظات العميل عند الحجز |
| reference_code | string | فريد — يُعرض للعميل كتأكيد |
| cancelled_at | datetime | اختياري — يُملأ عند الإلغاء |
| created_at | datetime | |
| updated_at | datetime | |


### Payment
| الحقل | النوع | ملاحظات |
|---|---|---|
| id | UUID/int | PK |
| booking | FK → Booking | one-to-one |
| amount | decimal | |
| currency | string | مثل `SAR` / `USD` |
| status | string | `pending` / `paid` / `failed` / `refunded` |
| payment_method | string | مثل `card` / `cash` / `online` |
| transaction_id | string | اختياري — معرّف العملية لدى بوابة الدفع |
| paid_at | datetime | اختياري — وقت نجاح الدفعة |
| created_at | datetime | |


## القيود الأساسية

**منع التضارب:**
- لا يمكن حجز نفس الموظف في أوقات متداخلة (تحقق من: start_time < booking.end_time AND end_time > booking.start_time لنفس الموظف في نفس اليوم).

**صحة البيانات:**
- `end_time` يجب أن يكون بعد `start_time` في Booking وWorkingHours.
- `break_end` يجب أن يكون بعد `break_start` في WorkingHours.
- `reference_code` فريد عالمياً.
- `(staff, day_of_week)` فريد في WorkingHours.
- `(staff, service)` فريد في StaffService.
- `(email, business)` فريد في Customer.

**قيود العلاقات:**
- لا يمكن إنشاء Booking لموظف خارج Business الخاصة بالحجز.
- الموظف يجب أن يقدّم الخدمة المحجوزة (يوجد سجل في StaffService).
- وقت الحجز يجب أن يقع ضمن WorkingHours النشطة للموظف في ذلك اليوم.

**قيود الظهور في صفحة الحجز:**
- لا تظهر Service غير مفعّلة (`is_active=false`).
- لا تظهر Service ليس لديها موظف نشط مرتبط بها.
- لا تُعرض أوقات خارج WorkingHours أو متداخلة مع حجز قائم.
