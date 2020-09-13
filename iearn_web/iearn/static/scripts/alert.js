
$(document).ready(function(){
    
    
    $('#confirm-deletion').click(function(){
        $.confirm({
            title: 'Patvirtinkite!',
            content: 'Ar tikrai norite ištrinti?',
            theme: 'light',
            useBootstrap: false,
            buttons: {
                confirm: {
                    text: 'TAIP',
                    action: function(){
                        $( "#delete" ).click();
                    }
                },
                cancel: {
                    text: 'ATŠAUKTI' // With spaces and symbols
                    
                }
            }
        });
        
    });

    $('#confirm-logout').click(function(){
        $.confirm({
            theme: 'light',
            title: 'Atsijungti?',
            content: 'Administratorius bus atjungtas po 5s.',
            autoClose: 'logoutUser|5000',
            buttons: {
                logoutUser: {
                    text: 'Atsijungti pačiam',
                    action: function () {
                        $('#logout')[0].click();
                        console.log($('#logout')[0]);
                    }
                },
                cancel: {
                    text: 'Atšaukti'
                }
            }
        });
    });
    
    $('#myalert').click(function(){
        $.alert({
            title: 'Alert!',
            content: 'Simple alert!'
        });
    });
    
});
