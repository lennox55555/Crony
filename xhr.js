const postBtn = document.getElementById('post-btn');

const sendHttpRequest =(method, url, data) => {
    const promise = new Promise((resolve, reject) =>{
        const xhr = new XMLHttpRequest();
        xhr.open(method, url);

        xhr.responseType = 'json';
        if(data) {
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
            // xhr.response.setRequestHeader("Access-Control-Allow-Origin", "*")
            xhr.setRequestHeader("Access-Control-Allow-Methods", "*")
            // xhr.setRequestHeader("Access-Control-Allow-Headers", "'Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token'")
            xhr.setRequestHeader("Access-Control-Allow-Headers", "*")
            xhr.withCredentials = false;
        }

        xhr.onload= () => {
            if (xhr.status >= 400) {
                reject(xhr.response);
            }
            else {
                resolve(xhr.response);
            }

        };

        xhr.onerror = () => {
            reject('Something went wrong');
        };

        xhr.send(JSON.stringify(data));
    });
    return promise;

};

const sendData = () => {
    sendHttpRequest('POST', 'https://7ev126d843.execute-api.us-west-2.amazonaws.com/v1/user', {
        email: 'test@test.com',
        password: 'tester'
    }).then(responseData => {
        console.log(responseData);
    }).catch(err => {
        console.log(err);
    });
};

postBtn.addEventListener('click', sendData);
