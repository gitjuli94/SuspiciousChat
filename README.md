# Suspicious Chat

This web application serves as a simple chat platform where logged-in users can add new messages, and admin users have the additional ability to delete messages. The application includes intentional security flaws, providing an opportunity to study and test vulnerabilities based on the OWASP Top 10:2021. The fixes to each security flaw are presented in the below sections. Two built-in users are included to facilitate functionality testing.

You can explore the code and the application on GitHub:
https://github.com/gitjuli94/SuspiciousChat


### Installation instructions:

To run the app, ensure that the Django framework is installed. Once set up, you can start the development server using:
```bash
python3 manage.py runserver
```

### Chosen flaws from OWASP Top 10:2021:
1) A01:2021 - Broken Access Control
2) A03:2021 - Injection
3) A05:2021 - Security Misconfiguration
4) A07:2021 - Identification and Authentication Failures
5) A09:2021 - Security Logging and Monitoring Failures

Below, each flaw is described along with its impact, the problematic code, and a suggested fix.

## FLAW 1: A01:2021 - Broken Access Control

### Problem
Non-admin users are able to delete messages due to a missing validation in the delete_chat function. This flaw allows unauthorized users to perform actions that should be restricted to administrators, violating access control policies.

### Fix
Add a verification step to ensure that only users with is_staff privileges (admin users) can delete messages. This can be achieved by adding a conditional check to verify the user's role before allowing access to the delete functionality.

Solution is to activate these out-commented lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#89
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#98
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#99

## FLAW 2: A03:2021 - Injection

### Problem
In the delete_chat function, raw SQL queries are executed using unvalidated user input. Specifically, the use of cursor.execute(f"DELETE FROM pages_chatmessage WHERE id = '{message_id}'") directly embeds the user-provided message_id into the SQL query string. This approach makes the application vulnerable to SQL injection attacks.

An attacker can craft a malicious message_id parameter to execute arbitrary SQL commands. For example:

message_id = "1; DROP TABLE pages_chatmessage; --"

### Fix
The Django ORM ensures that queries are safe from malicious input by handling escaping and parameterization. Replace the raw SQL queries with Django ORM commands, which automatically escape user input to prevent injection attacks.

Solution is to activate these out-commented lines and delete the raw connection.cursor() SQL query:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#93
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#94

## FLAW 3: A05:2021 - Security Misconfiguration

### Problem
The application includes hardcoded credentials, such as the admin account with the username admin and an easily guessable password admin. These credentials are exposed in the source code, making them publicly accessible.

Problems shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#17
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#25

### Fix
- Remove hardcoded credentials from the source code.
- Use environment variables to securely store usernames and passwords.
- Ensure passwords are strong and follow best practices, such as minimum length, inclusion of special characters, and avoiding dictionary words.
- Make the repository private to prevent unauthorized access.

## FLAW 4: A07:2021 - Identification and Authentication Failures

### Problem
Unauthenticated users can access the forum page and post messages. This allows unauthorized individuals to interact with the application, leading to potential misuse.

### Fix
Add the @login_required decorator to all functions related to the forum. This ensures that only authenticated users can access these pages or post new messages. Without this decorator, the application fails to enforce proper authentication checks.

Solution is to activate these out-commented lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#50
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#60
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#68
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#84

## FLAW 5: Security Logging and Monitoring Failures

### Problem
The application does not log login attempts, including failed attempts. This omission allows attackers to brute-force credentials without being detected, as no evidence of their attempts is captured.

### Fix
Implement a logging mechanism for login attempts using a custom Django model  FailedLoginAttempt. This model stores the following:

- The username entered.
- The IP address of the requester.
- The timestamp of the attempt.

You can acquire the IP address using the helper function added at the end of views.py.

Solution is to activate these out-commented lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#4
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#37
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#38

Activate class FailedLoginAttempt in models.py:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/models.py#8

Activate this get_ip function completely:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#102
