// Función ejemplo de hacer login, requiere como parametros solamente correo y contraseña
async function login(username, password) {
    let response = await axios.post('http://127.0.0.1:5000/login', {
            //Ambos datos se envían como parte de un body json
            "email": username,
            "password": password,
        });
    console.log(response);
}
// Devuelve un json coon 200 si los datos son correctos

//Para actualizar el puntaje se requiere email, true/false si atinó la respuesta, apouesta
async function updateScore(username, result, bet) {
    let response = await axios.post('http://127.0.0.1:5000/updateScore', {
            //También se envían como parte de un body
            "email": username,
            "result": result,
            "bet":1
        });
    console.log(response);
}
// No devuelve nada