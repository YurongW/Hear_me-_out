 $(function (){
            console.log("2222")
            var login = $.cookie('login_in');
            console.log(login);
            if(login == false || login == "undefined"){
                // {#window.location.href = "www.baidu.com"#}
                console.log("123123")
                // {#$(location).attr('href',"http://www.baidu.com"); #}
            }
        })