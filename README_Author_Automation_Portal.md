# Author Automation Portal - Complete Guide
### For Content Authors & Beginners (Zero Coding Knowledge)

**Last Updated:** August 2026

---

## 1. What is this Project?

This project helps **Content Authors** update AEM pages easily using Excel files — without opening AEM dialogs or CRXDE.

You can update:

1. **SEO Metadata** (Meta Title, Meta Description, Page Title, Canonical URL)
2. **Component Properties** (Title, Promo Banner, CTA, Hero Banner, etc.)

Even if the same component is used multiple times on a page, you can control which instance to update.

---

## 2. Project Structure (Important Files)

```
Author-Automation-Portal/
│
├── main.py                          ← Main entry point of the backend
├── requirements.txt                 ← List of required Python libraries
│
├── app/
│   ├── routes/                      ← API endpoints (URLs you call)
│   │   ├── upload.py
│   │   ├── seo_update.py            ← SEO Metadata update endpoint
│   │   ├── component_update.py      ← Component update endpoint
│   │   └── ... other routes
│   │
│   ├── services/                    ← Business logic (the real work happens here)
│   │   ├── seo_service.py           ← Handles SEO property updates
│   │   ├── component_service.py     ← Handles Component updates + Instance support
│   │   ├── component_ca_mapping.py  ← Mapping of Component Name + Field Name
│   │   └── ... other services
│   │
│   ├── validators/
│   ├── models/
│   └── database/
│
├── uploads/                         ← Temporary storage for uploaded Excel files
├── logs/
└── reports/
```

---

## 3. How to Start and Stop the Backend

### Step 1: Open Terminal
Go to the project folder (where `main.py` exists).

### Step 2: Activate Virtual Environment (if you have one)
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3: Install required libraries (only first time or when new libraries are added)
```bash
pip install -r requirements.txt
pip install requests pandas openpyxl
```

### Step 4: Start the Backend
```bash
uvicorn main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Open Swagger (Testing UI)
Open browser and go to:
```
http://127.0.0.1:8000/docs
```

### How to Stop the Backend
In the terminal press:
```
Ctrl + C
```

---

## 4. AEM Connection Settings

Currently the system connects to **local AEM**.

File: `app/services/seo_service.py` and `app/services/component_service.py`

```python
AEM_HOST = "http://localhost:8080"
AEM_USER = "admin"
AEM_PASSWORD = "admin"
```

**When moving to real server later**, you only need to change these three values.

---

## 5. SEO Metadata Update (CA Friendly)

### Endpoint
```
POST /seo-update
```

### Excel Format for Content Authors

| Page Path                          | Meta Title                          | Meta Description                     | Page Title          | Canonical URL                                      |
|------------------------------------|-------------------------------------|--------------------------------------|---------------------|------------------------------------------------------|
| /content/we-retail/ca/en/men       | 2027 Ram 1500 TRX SRT Title         | This is the new meta description     | Summer Collection   | https://www.ramtrucks.com/2027/ram-1500/trx.html     |

### How it works behind the scenes

| What CA writes       | What system updates in AEM     |
|----------------------|--------------------------------|
| Meta Title           | `jcr:title`                    |
| Meta Description     | `jcr:description`              |
| Page Title           | `pageTitle`                    |
| Canonical URL        | `cq:canonicalUrl`              |

The system automatically adds `/jcr:content` to the Page Path.

---

## 6. Component Update (CA Friendly)

### Endpoint
```
POST /component-update
```

### Excel Format for Content Authors

| Page Path                          | Component Name | Field Name     | New Value              | Instance |
|------------------------------------|----------------|----------------|------------------------|----------|
| /content/we-retail/ca/en/men       | Title          | Title          | Summer Sale 2026       | 1        |
| /content/we-retail/ca/en/men       | Title          | Title          | Another Title          | 2        |
| /content/we-retail/ca/en/men       | Promo Banner   | Heading        | Special Offer          | 1        |

### Important Rules

- `Instance` is **optional**. If not given, it updates the **first** matching component.
- Instance starts from **1**.
- Field Name is **case-insensitive** (`Title` or `title` both work).

---

## 7. How to Add a New Component (Very Important)

Whenever you want to support a new component, you only need to edit **one file**:

### File: `app/services/component_ca_mapping.py`

#### Example – Adding a new component called "Image"

```python
COMPONENT_CA_MAPPING = {

    "Title": {
        "resourceType": "weretail/components/content/title",
        "fields": {
            "Title": "jcr:title",
            "Type": "type"
        }
    },

    "Promo Banner": {
        "resourceType": "fca/components/content/promo-banner",
        "fields": {
            "Heading": "heading",
            "Description": "description"
        }
    },

    # ========== NEW COMPONENT ==========
    "Image": {
        "resourceType": "weretail/components/content/image",   # ← Get this from CRXDE
        "fields": {
            "Image": "fileReference",      # ← Real property name in AEM
            "Alt Text": "alt",
            "Title": "jcr:title"
        }
    }
}
```

### How to find the correct values

1. Open CRXDE → `http://localhost:8080/crx/de`
2. Go to any page that has the component
3. Click the component node
4. Look for:
   - `sling:resourceType` → This goes into `"resourceType"`
   - Property names on the right side → These go into `"fields"`

---

## 8. How to Add New Fields to an Existing Component

Just add a new entry inside the `"fields"` dictionary.

#### Example – Adding "Subtitle" field to Title component

```python
"Title": {
    "resourceType": "weretail/components/content/title",
    "fields": {
        "Title": "jcr:title",
        "Type": "type",
        "Subtitle": "subtitle"          # ← New field added
    }
}
```

Now Content Authors can use:

| Component Name | Field Name | New Value      |
|----------------|------------|----------------|
| Title          | Subtitle   | New Subtitle   |

---

## 9. Handling Image Components

Image components usually store the image path in a property called `fileReference`.

Example mapping:

```python
"Image": {
    "resourceType": "weretail/components/content/image",
    "fields": {
        "Image Path": "fileReference",
        "Alt Text": "alt",
        "Caption": "jcr:title"
    }
}
```

Excel example:

| Page Path                    | Component Name | Field Name  | New Value                              | Instance |
|------------------------------|----------------|-------------|----------------------------------------|----------|
| /content/we-retail/ca/en/men | Image          | Image Path  | /content/dam/we-retail/en/products/xxx.jpg | 1     |
| /content/we-retail/ca/en/men | Image          | Alt Text   | Beautiful product image                | 1        |

---

## 10. Same Component – Different Fields

You can update multiple fields of the same component in different rows.

Example:

| Page Path                    | Component Name | Field Name   | New Value          | Instance |
|------------------------------|----------------|--------------|--------------------|----------|
| /content/we-retail/ca/en/men | Title          | Title        | Main Heading       | 1        |
| /content/we-retail/ca/en/men | Title          | Type         | h2                 | 1        |
| /content/we-retail/ca/en/men | Promo Banner   | Heading      | Big Offer          | 1        |
| /content/we-retail/ca/en/men | Promo Banner   | Description  | Limited time only  | 1        |

---

## 11. Responsibility of Each Important File

| File                              | Responsibility                                      |
|-----------------------------------|-----------------------------------------------------|
| `main.py`                         | Starts the application and registers all routes     |
| `app/routes/seo_update.py`        | Receives Excel for SEO and calls seo_service        |
| `app/routes/component_update.py`  | Receives Excel for Components and calls component_service |
| `app/services/seo_service.py`     | Converts CA fields → AEM properties and updates page |
| `app/services/component_service.py`| Finds the correct component instance and updates it |
| `app/services/component_ca_mapping.py` | The brain – maps Component Name + Field Name to real AEM values |
| `uploads/`                        | Temporary folder where uploaded Excel files are stored |

---

## 12. Complete Testing Checklist

### SEO Testing
1. Create Excel with columns: `Page Path`, `Meta Title`, `Meta Description`, `Page Title`, `Canonical URL`
2. Go to Swagger → `/seo-update` → Upload file
3. Check the page properties in AEM

### Component Testing
1. Create Excel with columns: `Page Path`, `Component Name`, `Field Name`, `New Value`, `Instance`
2. Go to Swagger → `/component-update` → Upload file
3. Check the component in AEM Editor or CRXDE

---

## 13. Common Errors and Solutions

| Error Message                                      | Meaning & Solution                                      |
|----------------------------------------------------|---------------------------------------------------------|
| Missing required columns                           | Column names in Excel are wrong or have extra spaces    |
| Unknown Component Name                             | Component is not present in `component_ca_mapping.py`   |
| Unknown Field Name                                 | Field is not mapped under that component                |
| Could not find instance #X of component            | That instance number does not exist on the page         |
| AEM Error 404                                      | Wrong Page Path or component does not exist             |
| AEM Error 403                                      | Permission issue (check username/password)              |
| Connection error                                   | AEM is not running or wrong port                        |

---

## 14. Future Improvements (Ideas)

- Support for multi-value properties (Tags, Keywords)
- Support for updating multiple properties of one component in a single row
- Better reporting (download success/failure Excel)
- Authentication for the portal itself
- Move configuration (AEM URL, username, password) to a separate config file

---

## 15. Quick Reference – Commands

```bash
# Start backend
uvicorn main:app --reload

# Stop backend
Ctrl + C

# Install new library
pip install library_name

# Open Swagger
http://127.0.0.1:8000/docs
```

---

**End of Guide**

This README contains everything you need to run, test, and extend the Author Automation Portal.

Whenever you want to add a new component or new field in future, just update the mapping file `component_ca_mapping.py` — no other major code change is required.
