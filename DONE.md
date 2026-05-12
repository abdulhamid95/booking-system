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
