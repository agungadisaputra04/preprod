# DevOps Lab --- Git Final & Basic CI

## Tujuan

Dokumentasi ini merangkum fondasi DevOps yang sudah diimplementasikan
pada API lab: Git repository, dependency management,
configuration/secret, PostgreSQL test database, automated test, dan
GitHub Actions CI.

## 1. Application Handoff

Project:

``` text
preprod/
├── main.py
├── models.py
├── database.py
├── repository.py
├── requirements.txt
├── run.sh
├── .env
├── .env.example
└── tests/
    ├── conftest.py
    ├── test_api.py
    ├── test_crud.py
    └── schema.sql
```

Assessment:

  Item              Hasil
  ----------------- ------------------
  Runtime           Python 3.12
  Framework         FastAPI
  Server            Uvicorn
  Port              9000
  Database          PostgreSQL
  Test              pytest
  Dependency        requirements.txt
  Config template   .env.example
  Test schema       tests/schema.sql
  Entrypoint        main:app

Cara menjalankan aplikasi:

``` bash
source preprod/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000
```

## 2. Dependency

Dependency ditentukan oleh developer dan didefinisikan di
`requirements.txt`.

Contoh kondisi project:

``` text
fastapi==0.141.1
uvicorn==0.52.4
psycopg==3.3.5
python-dotenv==1.2.3
pytest==9.1.1
httpx==0.28.1
```

Semua dependency dipin versinya sehingga CI dapat membuat environment
yang lebih reproducible.

DevOps memastikan dependency tersebut dapat di-install pada
CI/deployment; DevOps tidak menebak atau menambahkan dependency aplikasi
tanpa alasan.

## 3. Configuration dan Secret

Aplikasi membutuhkan variable seperti:

``` text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

`.env.example` adalah template/kontrak configuration. Nilainya bukan
otomatis merupakan configuration production.

Prinsip:

``` text
Code
  +
Configuration
  +
Secret
```

dipisahkan.

`.env` lokal dapat berisi credential dan tidak boleh di-commit.

Production secret seharusnya disimpan menggunakan secret management,
bukan ditulis di repository.

## 4. Database

Aplikasi menggunakan PostgreSQL.

Database aplikasi:

``` text
api_lab
```

Database testing:

``` text
api_lab_test
```

Test schema tersedia pada:

``` text
tests/schema.sql
```

DevOps tidak perlu membuat ulang seluruh query `CREATE TABLE`.
Developer/DBA biasanya menyediakan schema atau migration; DevOps
memastikan migration/schema tersebut dapat dieksekusi secara repeatable
dalam pipeline.

Untuk aplikasi kompleks, migration tool lebih sesuai daripada mengelola
satu file `CREATE TABLE` besar.

## 5. Automated Test

Test berada di:

``` text
tests/
├── conftest.py
├── test_api.py
└── test_crud.py
```

Test lokal berhasil:

``` text
13 passed
```

CI menjalankan automated test tersebut.

Konsep:

``` text
Developer change
      ↓
git push
      ↓
CI
      ↓
pytest
      ↓
PASS / FAIL
```

## 6. Git Repository Hygiene

File runtime/development yang tidak seharusnya masuk Git di-ignore,
antara lain:

``` text
preprod/
__pycache__/
.pytest_cache/
nohup.out
*.log
.env
```

Sedangkan:

``` text
.env.example
```

boleh masuk repository karena tidak berisi secret production.

Sebelum push:

``` bash
git status
```

harus diperiksa.

## 7. Git Push dan Upstream

Jika branch lokal sudah memiliki upstream:

``` bash
git push
```

sudah cukup.

Bentuk eksplisit:

``` bash
git push origin main
```

Format:

``` text
git push <remote> <branch>
```

`origin` adalah nama remote dan `main` adalah branch tujuan.

## 8. Git History Security

Repository pernah memiliki credential hardcoded pada history lama.
History kemudian dibersihkan menggunakan `git-filter-repo` dan dilakukan
audit terhadap seluruh refs.

Prinsip penting:

> Secret yang pernah masuk Git history harus dianggap terekspos.
> Menghapusnya dari commit terbaru saja tidak cukup; credential yang
> terdampak perlu di-rotate/revoke.

## 9. Basic GitHub Actions CI

Workflow berada di:

``` text
.github/workflows/ci.yml
```

Trigger dasar:

``` yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```

Artinya CI berjalan ketika ada push ke `main` atau Pull Request menuju
`main`.

## 10. CI Runner

Workflow menggunakan:

``` yaml
runs-on: ubuntu-latest
```

GitHub menyediakan Ubuntu runner sementara untuk menjalankan job.

Secara konsep:

``` text
GitHub
   ↓
Ubuntu Runner
   ├── source code
   ├── Python
   ├── PostgreSQL
   └── pytest
```

## 11. PostgreSQL di CI

Karena aplikasi membutuhkan PostgreSQL, CI menyediakan PostgreSQL
sebagai service.

Konsep:

``` text
Ubuntu Runner
┌─────────────────────────────┐
│ Python                      │
│ pytest                      │
│ application source          │
│                             │
│ PostgreSQL 16               │
│ api_lab_test                │
└─────────────────────────────┘
```

Database ini khusus testing dan bukan production.

## 12. Urutan CI

Pipeline dasar:

``` text
git push
   ↓
GitHub Actions
   ↓
Checkout repository
   ↓
Setup Python 3.12
   ↓
Install requirements.txt
   ↓
Start/connect PostgreSQL
   ↓
Initialize tests/schema.sql
   ↓
Run pytest
   ↓
PASS / FAIL
```

Tujuan utamanya adalah membuat automated verification yang reproducible.

## 13. Eksperimen CI Failure → Fix → PASS

Untuk memahami CI, test sengaja diubah dari:

``` python
assert response.status_code == 200
```

menjadi:

``` python
assert response.status_code == 201
```

Aplikasi tetap mengembalikan HTTP 200 sehingga CI menghasilkan:

``` text
FAILED tests/test_api.py::test_root
1 failed, 12 passed
```

Perubahan kemudian diperbaiki kembali menjadi:

``` python
assert response.status_code == 200
```

dan CI berikutnya berhasil:

``` text
13 passed
```

Siklus yang dipelajari:

``` text
Change
  ↓
git push
  ↓
CI
  ↓
FAIL
  ↓
Fix
  ↓
git push
  ↓
CI
  ↓
PASS
```

## 14. Pembagian Tanggung Jawab

Model mental dasar:

  Developer / DBA              DevOps
  ---------------------------- --------------------------------
  Application code             CI/CD
  Business logic               Runtime environment
  Application dependencies     Infrastructure
  Automated tests              Deployment
  Database schema/migration    Secrets management
  Dockerfile jika disediakan   Monitoring
                               Backup/recovery infrastructure

Pembagian nyata dapat berbeda menurut organisasi.

Prinsipnya:

> Developer bertanggung jawab terhadap aplikasi dan kebutuhan teknis
> aplikasinya. DevOps bertanggung jawab terhadap automation, delivery,
> infrastructure, dan reliability process yang memungkinkan aplikasi
> dijalankan secara konsisten.

## 15. Mental Model

Ketika developer berkata:

> "Aplikasi sudah selesai, tolong deploy."

DevOps melakukan assessment:

``` text
Application
     ↓
Dependency
     ↓
Configuration
     ↓
Database
     ↓
Migration / Schema
     ↓
Tests
     ↓
How to run
     ↓
CI
```

Setelah CI berhasil:

``` text
CI
 ↓
Docker
 ↓
Docker image
 ↓
Container
 ↓
Registry
 ↓
CD
 ↓
Deployment
```

## 16. Status Pembelajaran

Selesai:

-   [x] Application handoff assessment
-   [x] Dependency/version awareness
-   [x] `.env` vs `.env.example`
-   [x] Database dependency
-   [x] Schema/migration responsibility
-   [x] Git repository hygiene
-   [x] Git push/upstream dasar
-   [x] Git history cleanup dasar
-   [x] GitHub Actions
-   [x] CI runner
-   [x] PostgreSQL service di CI
-   [x] Automated test
-   [x] CI PASS/FAIL cycle

Belum masuk:

-   [ ] Docker
-   [ ] Dockerfile
-   [ ] Docker Compose
-   [ ] Container registry
-   [ ] CD
-   [ ] Staging
-   [ ] Production deployment
-   [ ] Monitoring
-   [ ] Kubernetes

## 17. Next Topic

Tahap berikutnya adalah Docker.

Pertanyaan utama:

> Bagaimana aplikasi yang membutuhkan Python, dependency, virtual
> environment, dan configuration dapat dikemas agar dapat dijalankan
> secara konsisten di environment lain?

Urutan:

``` text
Application
    ↓
Dockerfile
    ↓
docker build
    ↓
Docker image
    ↓
docker run
    ↓
Container
```
