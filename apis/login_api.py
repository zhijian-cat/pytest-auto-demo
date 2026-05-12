from typing import Dict

class LoginAPI:
    """登录API"""

    @staticmethod
    def login(username:str, password:str) -> Dict:
        """执行登录-模拟实现"""
        #参数校验
        if not username:
            return {"code":400, "message":"用户名不能为空"}
        if not password:
            return {"code":400, "message":"密码不能为空"}
        
        #长度校验
        if len(username) > 100:
            return {"code":400, "message":"用户名长度超出限制"}
        if len(password) > 100:
            return {"code":400, "message":"用户密码超出长度限制"}
        
        #非法字符检测
        if '<' in username or '>' in username or 'script' in username.lower():
            return {"code": 400, "message": "用户名包含非法字符"}
        
        #SQL注册检测
        if "'" in username or '"' in username:
            return {"code":401, "message":"用户名或密码错误"}
        
        #用户验证
        valid_users = {
            "admin": "admin123",
            "user001": "pass123"
        }

        if username in valid_users:
            if valid_users[username] == password:
                return {"code": 200, "message": "登录成功", "token":f"token_{username}"}
            return {"code": 401, "message": "用户名或密码错误"}
        
        if username == "notexist":
            return {"code": 404, "message": "用户不存在"}
        
        return {"code": 401, "message": "用户名或密码错误"}

#便捷函数
def login_api(username:str, password:str) -> Dict:
    return LoginAPI.login(username, password)