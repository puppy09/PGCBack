# Ejemplos Postman - PGC Backend

**URL Base:** `https://proyectomedico.xyz:5000`  
**Nota:** Desactiva SSL verification en Postman (Settings > SSL certificate verification: OFF)

---

## 1. Login

**POST** `https://proyectomedico.xyz:5000/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "contra": "contraseña123"
}
```

---

## 2. Predecir PGC (Requiere Token)

**POST** `https://proyectomedico.xyz:5000/predecir`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer TU_TOKEN_AQUI
```

**Body:**
```json
{
  "altura": 175,
  "peso": 70,
  "pecho": 95,
  "abdomen": 85,
  "cadera": 100
}
```

