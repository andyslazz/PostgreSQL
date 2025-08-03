# PostgreSQL Lab - Computer Engineering Laboratory

## 📌 วัตถุประสงค์
- เข้าใจการใช้งานฐานข้อมูล **PostgreSQL**
- ฝึกใช้ **PGADMIN** จัดการฐานข้อมูล PostgreSQL
- ทดลองเขียนโปรแกรมภาษา **Python** เพื่อเชื่อมต่อ PostgreSQL ด้วย SQLAlchemy

---

## 🔧 Lab Outline

### 1. 📖 Introduction to PostgreSQL
- ศึกษาความรู้พื้นฐานเกี่ยวกับ PostgreSQL
- แหล่งศึกษาเพิ่มเติม:
  - https://www.postgresql.org/docs/16/index.html
  - https://www.geeksforgeeks.org/postgresql-tutorial/?ref=lbp


### 2. 🐳 PostgreSQL with Docker

#### 2.1 สร้างไฟล์ `docker-compose.yml`
- กำหนด container สำหรับ `postgres` และ `pgadmin`
- ตั้งค่า environment variables, ports, volumes ฯลฯ

#### 2.2 เริ่มการทำงาน
```bash
docker compose up -d
docker compose ps
```


### 3. 🖥️ PGADMIN

#### 3.1 เปิด PGAdmin
- URL: `http://localhost:7080`

#### 3.2 Login
- Username: `coe@local.db`
- Password: `CoEpasswd`

#### 3.3 Database Registration
- Register database: `coedb` ด้วย user `coe` และ password `CoEpasswd`

#### 3.4 สร้าง Table และเพิ่มข้อมูล
- ชื่อ Table: `activities`
- เพิ่ม columns ตามที่กำหนด
- เพิ่มข้อมูลจำนวน (รหัสนักศึกษา mod 5) + 3 rows


#### 3.5 ใช้ SQL จัดการข้อมูล
- ทดลองคำสั่ง SQL:
  - `INSERT`
  - `UPDATE`
  - `DELETE`


### 4. 🐍 SQLAlchemy

#### 4.1 ทำความรู้จัก SQLAlchemy
- ศึกษาจาก: https://www.sqlalchemy.org/


#### 4.2 รันตัวอย่างโปรแกรม
- โหลดโค้ดจาก `psunote.tar.gz`
- ติดตั้ง dependency และรันแอป Flask:
```bash
pip install -r requirements.txt
python psunote/noteapp.py
```
- เปิดเบราว์เซอร์ที่ `http://localhost:5000`

#### 4.3 แก้ไขโค้ดให้สามารถ:
- แก้ไข Note
- แก้ไข Tag