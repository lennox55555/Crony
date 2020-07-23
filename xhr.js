const postBtn = document.getElementById('post-btn');

const sendHttpRequest =(method, url, data) => {
    const promise = new Promise((resolve, reject) =>{
        const xhr = new XMLHttpRequest();
        xhr.open(method, url);

        xhr.responseType = 'json';
        if(data) {
            xhr.setRequestHeader('Content-Type', 'application/json');
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
    sendHttpRequest('POST', ' arn:aws:execute-api:us-west-2:768445991427:7ev126d843/*/POST/user', {
        email: 'test@test.com',
        password: 'tester'
    }).then(responseData => {
        console.logz(responseData);
    }).catch(err => {
        console.log(err);
    });
};

postBtn.addEventListener('click', sendData);
