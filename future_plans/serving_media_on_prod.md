# I have to make below changes while deploying on production using Nginx
In production, Django **does not** serve static or media files (like documents) by itself. Instead, you should configure a web server like **Nginx** or **Apache** to serve files directly from your `documents/` directory. The code you mentioned for serving files during development (`if settings.DEBUG`) only works for the development environment.

Here's how you can handle file serving in production:

### 1. **Remove `static()` for Production**
You can keep the `static()` configuration under the `if settings.DEBUG:` block to serve documents during development, but **do not** rely on Django to serve files in production.

In production, this section should remain as is:

```python
# project_root/urls.py

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your other URL patterns
]

# Serve files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

This means Django will **not serve media files in production**. You will need to configure your web server to handle this.

### 2. **Configure a Web Server to Serve Files in Production**

In production, a web server (like **Nginx** or **Apache**) should serve the files directly from the `documents/` directory. Below are configurations for both **Nginx** and **Apache**.

#### Nginx Configuration

To configure Nginx to serve the `documents/` directory, you'll need to update your Nginx configuration file (often located in `/etc/nginx/sites-available/your-site.conf` or similar).

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Proxy to your Django app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve the files in the documents/ directory directly
    location /documents/ {
        alias /path/to/your/project/documents/;  # Absolute path to your documents directory
        autoindex off;
    }

    # Static files (CSS, JS, images)
    location /static/ {
        alias /path/to/your/project/static/;
    }
}
```

- The `location /documents/` block serves files from your `documents/` directory.
- Replace `/path/to/your/project/documents/` with the actual path to your `documents/` directory.

#### Apache Configuration

For **Apache**, you can use the following configuration to serve files from the `documents/` directory. You can add this to your Apache virtual host configuration file.

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/your/project

    # Proxy all requests to Django except for static and media files
    ProxyPass /static/ !
    ProxyPass /documents/ !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    # Serve static files (CSS, JS, images)
    Alias /static/ /path/to/your/project/static/

    # Serve the files in the documents/ directory directly
    Alias /documents/ /path/to/your/project/documents/
    <Directory /path/to/your/project/documents/>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

- The `Alias /documents/ /path/to/your/project/documents/` directive serves files from the `documents/` directory.
- Replace `/path/to/your/project/documents/` with the actual path to your `documents/` directory.

### 3. **File Permissions**

Ensure that the web server user (like `www-data` for Nginx/Apache) has read access to the `documents/` directory. If permissions are too restrictive, the web server won’t be able to serve the files.

You can adjust permissions as needed:

```bash
sudo chown -R www-data:www-data /path/to/your/project/documents/
sudo chmod -R 755 /path/to/your/project/documents/
```

### 4. **Django Settings for Production**

In production, `DEBUG` should always be set to `False`, and you should configure your settings accordingly to handle static and media files. Make sure to also set the `ALLOWED_HOSTS` and other security settings properly.

```python
# settings.py

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com']

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Media files (uploaded documents)
MEDIA_URL = '/documents/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'documents/')
```

### 5. **Testing the Configuration**

After setting up the Nginx or Apache configuration:
1. Restart your web server:
   - For Nginx: `sudo systemctl restart nginx`
   - For Apache: `sudo systemctl restart apache2`
2. Test the file URLs (e.g., `http://your-domain.com/documents/madhu_babu/your-file.pdf`) to ensure they are served correctly.

### Conclusion

In production:
- **Django should not serve media files directly**; instead, you should configure a web server like Nginx or Apache to handle this.
- You can use `/documents/` as your base directory for uploaded files and serve them directly using the web server.
- Adjust file permissions to ensure the web server can read the files.

### Suggestions:
**a.** Set up a CDN (Content Delivery Network) to cache and serve files more efficiently, especially for large-scale applications.  
**b.** Implement file size restrictions or security measures to ensure proper handling of uploads in production.