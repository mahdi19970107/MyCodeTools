<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <title>خوش آمدید - ورود به وردپرس</title>
    <style>
        body {
            font-family: 'Tahoma', sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        
        .login-box {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 350px;
            text-align: center;
        }
        
        h1 {
            color: #1a73e8;
            margin-bottom: 1.5rem;
        }
        
        .input-group {
            margin-bottom: 1rem;
            text-align: right;
        }
        
        input {
            width: 100%;
            padding: 0.8rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 0.5rem;
        }
        
        button {
            background-color: #1a73e8;
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        
        button:hover {
            background-color: #1557b0;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>خوش آمدید</h1>
        <form method="post" action="wp-login.php">
            <div class="input-group">
                <label for="user_login">نام کاربری یا ایمیل</label>
                <input type="text" name="log" id="user_login" required>
            </div>
            
            <div class="input-group">
                <label for="user_pass">رمز عبور</label>
                <input type="password" name="pwd" id="user_pass" required>
            </div>
            
            <input type="hidden" name="redirect_to" value="<?= $_SERVER['HTTP_REFERER'] ?>">
            <button type="submit">ورود به سیستم</button>
        </form>
    </div>
</body>
</html>