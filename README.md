# 🔒 Image Upload Management with S3 and Pre-Signed URLs

This project implements a secure and efficient mechanism to handle image uploads to an Amazon S3 bucket using pre-signed URLs. It features a Python-powered backend and a frontend that allows users to upload images directly to the bucket—without exposing AWS credentials.

---

## 🚀 Functionality

1. 🔗 Pre-signed URL Generation

- Generates a time-limited URL that grants temporary upload permissions directly to S3.
- The expiration time for the URL is configurable (default: 1 hour).

2. 🛡️ Secure Image Uploading

- Users can upload images to the bucket without requiring AWS credentials.
- The backend validates requests and issues pre-signed URLs only to authorized clients.

3. 🛠️ Technologies Used

- Custom security policies restrict access to the bucket.
- Only uploads via pre-signed URLs or trusted referrers are permitted

## 🛠️ Technologies Used

## 🛠️ Technologies Used

- 👨‍💻 **Backend**: Python – [![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white&style=flat-square)](https://fastapi.tiangolo.com/) & [![Boto3](https://img.shields.io/badge/Boto3-FF9900?logo=amazonaws&logoColor=white&style=flat-square)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
  
- ☁️ **Cloud Services**: [![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/s3/)

  
- 🚀 **Backend Deployment**: [![Render](https://img.shields.io/badge/Render-3A3A3A?logo=render&logoColor=white&style=flat-square)](https://render.com/)
  
- 🗄️ **Database**: [![MongoDB Atlas](https://img.shields.io/badge/MongoDB_Atlas-47A248?logo=mongodb&logoColor=white&style=flat-square)](https://www.mongodb.com/cloud/atlas)

