$(function (){
    let allUsers = $('#user');

    $.ajax({
        type: 'GET',
        url: 'https://7ev126d843.execute-api.us-west-2.amazonaws.com/v1/user',
        success: function(allUsers){
            $.each(allUsers, function(i, user){
               $allUsers.append('<li>id: ' + user.id + ', name: ' + user.firstName + ' ' + user.lastName + '</li>');
            });
        }
    })
});