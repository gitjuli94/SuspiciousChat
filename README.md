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
Non-admin users are able to delete messages due to a missing validation in the delete_chat function. This flaw allows unauthorized users to perform actions that should be restricted to administrators, violating access control policies. If non-admin users can delete messages, they can potentially disrupt the application's functionality by removing important content. Furthermore, this can cause loss of data integrity and lead to frustration among legitimate users, as no proper checks are in place to prevent such unauthorized actions.

### Fix
Add a verification step to ensure that only users with is_staff privileges (admin users) can delete messages. This can be achieved by adding a conditional check to verify the user's role before allowing access to the delete functionality.

Solution is to activate these out-commented lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L89
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L98
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L99

## FLAW 2: A03:2021 - Injection

### Problem
In the delete_chat function, raw SQL queries are executed using unvalidated user input retrieved from a query parameter. Because no validation or sanitization is performed, an attacker can craft a malicious message_id parameter to execute arbitrary SQL commands. For example:

Attacker's input on the address bar:
```bash
http://127.0.0.1:8000/delete_chat/?id=0 OR 1=1
```
Resulting SQL:
```bash
DELETE FROM pages_chatmessage WHERE id = 0 OR 1=1
```
Causing the query to match all rows in the table, effectively deleting all messages.

### Fix
Include the message_id as a typed URL path parameter and enforce it as an integer using <int:message_id>. This blocks malicious input like SQL code from reaching the database, as only valid integers are accepted.

Activate:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/urls.py#10

Comment out:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/urls.py#9

The Django ORM ensures that queries are safe from malicious input by handling escaping and parameterization. Replace the raw SQL queries with Django ORM commands, which automatically escape user input to prevent injection attacks.

Solution is to activate these out-commented lines and delete the raw connection.cursor() SQL query:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L85
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L95
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L96

Comment out:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L86
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L90
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L93
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L94

## FLAW 3: A05:2021 - Security Misconfiguration

### Problem
The application includes hardcoded credentials, such as the admin account with the username admin and an easily guessable password admin. These credentials are exposed in the source code, making them publicly accessible. This makes it easy for attackers to gain access to the admin account and exploit its elevated privileges. Hardcoding sensitive information in the source code not only compromises security but also makes it difficult to change credentials later without modifying and redeploying the application.

Problems shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L17
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L25

### Fix
- Remove hardcoded credentials from the source code.
- Use environment variables to securely store usernames and passwords.
- Ensure passwords are strong and follow best practices, such as minimum length, inclusion of special characters, and avoiding dictionary words.
- Make the repository private to prevent unauthorized access.

## FLAW 4: A07:2021 - Identification and Authentication Failures

### Problem
Unauthenticated users can access the forum page and post messages. This allows unauthorized individuals to interact with the application, leading to potential misuse. Such unrestricted access could result in spamming, inappropriate content, or even malicious actions like exploiting vulnerabilities in the forum. Without authentication, it is impossible to associate forum activity with legitimate users, making the application less reliable and less secure.

### Fix
Add the @login_required decorator to all functions related to the forum. This ensures that only authenticated users can access these pages or post new messages. Without this decorator, the application fails to enforce proper authentication checks.

Solution is to activate these out-commented lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L50
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L60
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L68
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L84

## FLAW 5: Security Logging and Monitoring Failures

### Problem
The application does not log login attempts, including failed attempts. This omission allows attackers to brute-force credentials without being detected, as no evidence of their attempts is captured. Without proper logging, it is difficult for administrators to detect suspicious activity or respond to potential attacks. Logging failed login attempts can serve as an early warning system to identify potential brute force attacks or unauthorized access attempts.

### Fix
Implement a logging mechanism for login attempts using a custom Django model  FailedLoginAttempt. This model stores the following:

- The username entered.
- The IP address of the requester.
- The timestamp of the attempt.

You can acquire the IP address using the helper function added at the end of views.py.

Solution is to activate these out-commented lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L4
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L37
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L38

Activate class FailedLoginAttempt in models.py:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/models.py#L8

Activate this get_ip function completely:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#L102
