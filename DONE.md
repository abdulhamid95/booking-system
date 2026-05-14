# DONE.md

> هذا الملف يحتوي على المهام المنجزة والمعتمدة.  
> لا تُضاف مهمة هنا إلا بموافقة صريحة من مدير المشروع.

---

## EPIC-01: إعداد المشروع والبنية الأساسية

---

### TASK-001-A: تثبيت المتطلبات وإنشاء البيئة الافتراضية

**الأولوية:** P1  
**النوع:** Setup  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إنشاء virtual environment باستخدام `python -m venv venv`
- تثبيت: `Django 5.2.14`, `djangorestframework 3.17.1`, `python-decouple 3.8`, `psycopg2-binary 2.9.12`
- إنشاء ملف `requirements.txt`

- [x] منجزة

---

### TASK-001-B: إنشاء هيكل مشروع Django

**الأولوية:** P1  
**النوع:** Setup  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- تنفيذ `django-admin startproject core .`
- التحقق من أن `manage.py check` و`runserver` يعملان بدون أخطاء

- [x] منجزة

---

### TASK-001-C: إنشاء التطبيقات الأساسية

**الأولوية:** P1  
**النوع:** Setup  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إنشاء التطبيقات: `accounts`, `businesses`, `services`, `staff`, `bookings`
- تسجيل جميعها في `INSTALLED_APPS` داخل `core/settings.py`

- [x] منجزة

---

### TASK-001-D: إعداد ملف البيئة (.env)

**الأولوية:** P1  
**النوع:** Setup  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إنشاء `.env` يحتوي على `SECRET_KEY`, `DEBUG`, وإعدادات PostgreSQL
- إنشاء `.env.example` كنموذج للمطورين
- إنشاء `.gitignore` مع إدراج `.env` فيه
- تعديل `core/settings.py` لقراءة جميع الإعدادات الحساسة عبر `python-decouple`

- [x] منجزة

---

### TASK-001-E: إعداد Django REST Framework

**الأولوية:** P1  
**النوع:** Setup  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إضافة `rest_framework` إلى `INSTALLED_APPS`
- إضافة إعدادات `REST_FRAMEWORK` في `core/settings.py` مع `IsAuthenticatedOrReadOnly` كصلاحية افتراضية

- [x] منجزة

---

### TASK-002: إعداد قاعدة البيانات

**الأولوية:** P1  
**النوع:** Backend  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- تثبيت `psycopg2-binary` في `requirements.txt`
- إعداد متغيرات قاعدة البيانات في `.env` (`DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
- تعديل `core/settings.py` لقراءة إعدادات PostgreSQL عبر `python-decouple` بدلاً من `dj-database-url`
- تشغيل `python manage.py migrate` بنجاح
- التحقق من `python manage.py check --database default` بدون أخطاء

**ملاحظة التنفيذ:**  
استُخدم `python-decouple` مع متغيرات منفصلة بدلاً من `dj-database-url` + `DATABASE_URL` — كلاهما مقبول، والنهج الفعلي موثّق هنا.

- [x] منجزة

---

## EPIC-02: الحسابات وتسجيل الدخول

---

### TASK-003: إنشاء نظام المستخدمين

**الأولوية:** P1  
**النوع:** Backend  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إنشاء `CustomUser` model في `accounts/models.py` يرث من `AbstractBaseUser + PermissionsMixin` مع تسجيل دخول بالبريد الإلكتروني
- إنشاء `CustomUserManager` في `accounts/managers.py` يدعم `create_user` و `create_superuser`
- تعيين `AUTH_USER_MODEL = 'accounts.CustomUser'` في `core/settings.py`
- إضافة `rest_framework.authtoken` إلى `INSTALLED_APPS` وإعداد `TokenAuthentication`
- إنشاء `accounts/serializers.py`: `RegisterSerializer`, `LoginSerializer`, `UserProfileSerializer`
- إنشاء 4 API endpoints في `accounts/views.py`: register، login، logout، me
- إنشاء `accounts/urls.py` وربطه في `core/urls.py` على `/api/auth/`
- تسجيل `CustomUser` في Django Admin عبر `accounts/admin.py`
- إنشاء migration: `accounts/migrations/0001_initial.py`

**ملاحظة التنفيذ:**  
قاعدة البيانات PostgreSQL تحتاج إلى إعادة تهيئة (DROP SCHEMA ثم migrate) بسبب تعارض تاريخ الـ migrations مع `AUTH_USER_MODEL` الجديد.

- [x] منجزة

---

### TASK-004: تسجيل منشأة جديدة مع حساب مسؤول

**الأولوية:** P1  
**النوع:** Backend / API  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إنشاء `Business` model في `businesses/models.py` بـ `OneToOneField` إلى `CustomUser` وحقول: `name`, `business_type`, `phone`, `address`, `created_at` مع `TextChoices` لأنواع المنشآت (salon / clinic / other)
- إنشاء `businesses/serializers.py` يحتوي على `BusinessSerializer` (قابل للإعادة في EPIC-03)
- إضافة `BusinessRegistrationSerializer` في `accounts/serializers.py` مع `@transaction.atomic` وvalidation على تكرار البريد
- إضافة `BusinessRegisterView` في `accounts/views.py` — يُنشئ المستخدم والمنشأة atomically ويُعيد token + user + business
- إضافة route `POST /api/auth/register/business/` في `accounts/urls.py`
- تسجيل `Business` في Django Admin عبر `businesses/admin.py`
- إنشاء migration: `businesses/migrations/0001_initial.py`
- `manage.py check` نظيف بدون أخطاء

**ملاحظة التنفيذ:**  
هذه المهمة غطّت أيضاً TASK-005 (نموذج Business) — لا حاجة لتكراره لاحقاً.  
تشغيل `migrate` يتطلب إعادة تهيئة PostgreSQL أولاً (راجع ملاحظة TASK-003).

- [x] منجزة

---

## EPIC-03: إدارة المنشأة

---

### TASK-005: إنشاء نموذج المنشأة Business

**الأولوية:** P1  
**النوع:** Backend  
**تاريخ الإنجاز:** 2026-05-12

**ملاحظة:** أُنجزت ضمن TASK-004 — راجع توثيقها أعلاه.

- [x] منجزة (ضمن TASK-004)

---

### TASK-006: حماية بيانات كل منشأة

**الأولوية:** P1  
**النوع:** Backend / Security  
**تاريخ الإنجاز:** 2026-05-12

**ما تم تنفيذه:**
- إنشاء `IsBusinessOwner` permission class في `businesses/permissions.py` — يُعيد `403` إن لم يكن للمستخدم منشأة
- إنشاء `BusinessScopedMixin` في `businesses/mixins.py` — يُطبَّق على كل view إداري ويوفر `get_business()` للفلترة الآمنة
- إنشاء `BusinessProfileView` في `businesses/views.py` — `GET/PATCH /api/businesses/me/` كأول تطبيق فعلي للمixin
- إنشاء `businesses/urls.py` وربطه في `core/urls.py`
- الـ `404` على الوصول العرضي مضمون تلقائياً: الـ queryset مُقيَّد بـ `filter(business=self.get_business())`
- `manage.py check` نظيف بدون أخطاء

**ملاحظة التنفيذ:**  
هذه المهمة أنشأت البنية التحتية الأمنية — EPIC-04/05/06 ستُطبّقها بوراثة `BusinessScopedMixin` في كل view.

- [x] منجزة

---

## EPIC-04: إدارة الخدمات

---

### TASK-007: إنشاء نموذج الخدمة Service

**الأولوية:** P1  
**النوع:** Backend  
**تاريخ الإنجاز:** 2026-05-14

**ما تم تنفيذه:**
- إنشاء `Service` model في `services/models.py` بحقول: `business`, `name`, `description`, `duration_minutes`, `price`, `is_active`, `created_at`
- ربط الخدمة بالمنشأة عبر `ForeignKey → Business`
- تسجيل النموذج في Django Admin عبر `services/admin.py`
- إنشاء وتشغيل migration

**الفرع:** `epic-04/service-model`

- [x] منجزة

---

### TASK-008: إنشاء واجهة إدارة الخدمات

**الأولوية:** P1  
**النوع:** Frontend / Admin  
**تاريخ الإنجاز:** 2026-05-14

**ما تم تنفيذه:**
- إعداد واجهة Django Admin لإدارة الخدمات (إضافة، تعديل، تعطيل)
- دعم الفلترة حسب الحالة (`is_active`) والمنشأة
- تعطيل الخدمة عبر `is_active = False` بدل الحذف النهائي
- الخدمات المعطلة لا تظهر في صفحة الحجز العامة

**الفرع:** `epic-04/service-admin-ui`

- [x] منجزة

---

## EPIC-05: إدارة الموظفين

---

### TASK-009: إنشاء نموذج الموظف StaffMember

**الأولوية:** P1  
**النوع:** Backend  
**تاريخ الإنجاز:** 2026-05-14

**ما تم تنفيذه:**
- إنشاء `StaffMember` model في `staff/models.py` بحقول: `business`, `name`, `email`, `phone`, `is_active`
- ربط الموظف بالمنشأة عبر `ForeignKey → Business`
- تسجيل النموذج في Django Admin عبر `staff/admin.py`
- إنشاء وتشغيل migration

**الفرع:** `epic-05/staff-model`

- [x] منجزة

---

### TASK-010: ربط الموظفين بالخدمات

**الأولوية:** P1  
**النوع:** Backend  
**تاريخ الإنجاز:** 2026-05-14

**ما تم تنفيذه:**
- إضافة `ManyToManyField → Service` في `StaffMember` تحت حقل `services`
- إنشاء وتشغيل migration
- يمكن لكل موظف تقديم أكثر من خدمة، ويمكن لكل خدمة أن تُقدَّم من أكثر من موظف

**الفرع:** `epic-05/staff-services-link`

- [x] منجزة

---

### TASK-011: إنشاء واجهة إدارة الموظفين

**الأولوية:** P1  
**النوع:** Frontend / Admin  
**تاريخ الإنجاز:** 2026-05-14

**ما تم تنفيذه:**
- إعداد واجهة Django Admin لإدارة الموظفين (إضافة، تعديل، تعطيل)
- دعم اختيار الخدمات المرتبطة بالموظف عبر `filter_horizontal`
- دعم الفلترة حسب الحالة (`is_active`) والمنشأة
- الموظفون المعطلون لا يظهرون في صفحة الحجز العامة

**الفرع:** `epic-05/staff-admin-ui`

- [x] منجزة
