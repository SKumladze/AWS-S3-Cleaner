# 🧹 AWS S3 Cleaner

A simple Python CLI tool to clean up AWS S3 buckets by deleting:

- Old object versions
- Incomplete multipart uploads

Helps reduce AWS storage costs and keep your environment clean.

This tool deletes data. Use responsibly. No warranties for any data loss.

---

## 🚀 Features

- ✅ Delete **old object versions** (requires versioning enabled)
- ✅ Delete **incomplete multipart uploads**
- 📆 Target items older than a given number of days
- 🔐 Uses AWS credentials from profile, env vars, or IAM role
- 🧪 Safe and testable (start with short retention like `--days 1`)

---

## 📦 Tech Stack

- Python 3.7+
- boto3 (AWS SDK for Python)
- python-dateutil

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/SKumladze/AWS-S3-Cleaner.git
cd s3-cleaner
```

Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

🧑‍💻 Usage
```bash
python cleaner.py <bucket-name> [OPTIONS]
```

✅ Options

Option	    Description

--versions	Delete old object versions
--uploads	Delete incomplete multipart uploads
--days N	Only delete items older than N days (default: 30)


📌 Examples
```bash
python cleaner.py my-bucket --versions --uploads --days 45
python cleaner.py my-bucket --uploads --days 7
python cleaner.py my-bucket --versions --days 60
```

Required AWS IAM Permissions
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:ListBucket",
    "s3:ListBucketVersions",
    "s3:ListBucketMultipartUploads",
    "s3:DeleteObjectVersion",
    "s3:AbortMultipartUpload"
  ],
  "Resource": [
    "arn:aws:s3:::your-bucket-name",
    "arn:aws:s3:::your-bucket-name/*"
  ]
}
```

🧠 Pro Tips

🧪 Start with a low --days value (like 1 or 2) to test without risk.

🔁 Schedule it with cron, AWS Lambda, or CI/CD to keep S3 clean over time.

📊 Combine with S3 Lifecycle Rules for full storage optimization.

🛑 Double-check everything before using on production buckets — especially if MFA Delete or compliance retention is enabled.