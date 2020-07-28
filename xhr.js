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
<<<<<<< Updated upstream

    sendHttpRequest('POST', 'https://7ev126d843.execute-api.us-west-2.amazonaws.com/v1/user', {
=======
    sendHttpRequest('POST', 'https://crony-hiking.s3-us-west-2.amazonaws.com/index.html', {
>>>>>>> Stashed changes
        email: 'test@test.com',
        password: 'tester'
    }).then(responseData => {
        console.logz(responseData);
    }).catch(err => {
        console.log(err);
    });
};

postBtn.addEventListener('click', sendData);


function fn1()
{
    var str = document.getElementById("text11").value;
    alert("The Account for "+str +" has been created.")
    $(function () {
        var $orders = $('#orders');
        var $text11 = $('text11');
        var $text10 = $('text10');
        var $text9 = $('text9');
        var $text8 = $('text8');
        var $text7 = $('text7');
        var $text6 = $('text6');
        var $text5 = $('text5');
        var $text4 = $('text4');
        var $text3 = $('text3');
        var $text2 = $('text2');
        var $text1 = $('text1');

        $('#post-btn').on('click', function () {

            var order = {
                text11: $text11.val(),
                text10: $text10.val(),
                text9: $text9.val(),
                text8: $text8.val(),
                text7: $text7.val(),
                text6: $text6.val(),
                text5: $text5.val(),
                text4: $text4.val(),
                text3: $text3.val(),
                text2: $text2.val(),
                text1: $text1.val()
            };

            $.ajax({
                type: 'POST',
                url: 'https://7ev126d843.execute-api.us-west-2.amazonaws.com/v1/user/?',
                data: order,
                success: function(newOrder) {
                    $orders.append('<li>my order</li>');
                }
            });
        });

    });
}