from fastapi import FastAPI, status, HTTPException, Depends 
from fastapi.security import HTTPBasic, HTTPBasicCredentials #----> seguridad
import secrets

#seguridad http basic
security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credentials.username, "IsabelNavarrete")
    contrasena_correcta = secrets.compare_digest(credentials.password, "123456")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = " Credenciales no válidas"
        )
    return credentials.username 