
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/img/top.ico">

    <title>Quiz.it</title>

      
    <!-- Bootstrap core CSS -->
    <link href="vendor/bootstrap-4.3.1/css/bootstrap.css" rel="stylesheet">

    <!-- Custom styles for this template -->
     <link  type="text/css" rel="stylesheet" href="css/game.css"> 
      
      
      <!-- jquery -->

      <link rel="stylesheet" href="//apps.bdimg.com/libs/jqueryui/1.10.4/css/jquery-ui.min.css">
  <script src="//apps.bdimg.com/libs/jquery/1.10.2/jquery.min.js"></script>
  <script src="//apps.bdimg.com/libs/jqueryui/1.10.4/jquery-ui.min.js"></script>
      
      
      <script>
        $( function() {
            $(".progress-bar").animate({
                width: "100%"
            }, 12000);
            
            //wrongAnswer();
            } );
  </script>
      
  </head>

  <body class="text-center" onload="start()">
      
      
      
     <nav class="navbar navbar-expand-lg navbar-light bg-light">
         <p>&lt Back</p> 
         <p id="quizName">Quiz 1</p>
         <p>100 pts</p>

    </nav>
      
      <div id="question-div" class="bg-custom4 question-div">
        <h4 class="h4 mb-4 font-weight-light" id="category"></h4>
          <h4 class="h4 mb-4 font-weight-normal" id="question"></h4>
      
          <div class="progress">
            <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
      </div>
      
        <button onclick="check('0')" class="btn btn-lg btn-block font-weight-light" id="opt0"></button>
        <button onclick="check('1')" class="btn btn-lg btn-block font-weight-light" id="opt1"></button>
        <button onclick="check('2')" class="btn btn-lg btn-block font-weight-light" id="opt2"></button>
        <button onclick="check('3')" class="btn btn-lg btn-block font-weight-light" id="opt3"></button>
      
      <div></div>
       
      
    <form class="form-signin" action="" method="post" id="form-question">
        
        <!---Buttons-->


        
      
    </form>
      
      
   <div class="d-flex p-2">
       <p class="mb-4 font-weight-normal" id="bet">Current bet: 0 pts</p>
       <div class="d-flex p-2 bet_div">
       <img class="bet_icon" src="img/minus.png" onclick="minusBet()">
        <img class="bet_icon" src="img/plus.png" onclick="plusBet()">
       
        </div>
      
      
      
      
    </div>
      
      <script src="vendor/jquery/jquery-3.5.1.min.js"></script>
      <script src="vendor/bootstrap-4.3.1/js/bootstrap.min.js"></script>
      
      <p class="mt-5 mb-3 text-muted">&copy; COVID-Games 2020</p>
      
      <script>
          
    /**** Loads question from backend on load *****/ 
    var correct;
    var bet;
    function start() {
        
        bet = 0;
        
        
        question =  JSON.parse(httpGet("http://127.0.0.1:5000/getQuestions"));
        document.getElementById("category").innerHTML = question.category;
        document.getElementById("question").innerHTML = question.question;
        document.getElementById("opt0").innerHTML = question.possible_answers[0];
        document.getElementById("opt1").innerHTML = question.possible_answers[1];
        document.getElementById("opt2").innerHTML = question.possible_answers[2];
        document.getElementById("opt3").innerHTML = question.possible_answers[3];
        
        correct = question.correct_answer;
        
        
        console.log(correct);
    }
    
    function httpGet(theUrl){
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }
          
        
    function check(option){
        if(option == correct)
            console.log("correct!"); //rightAnswer();
        else
            console.log("false!"); //wrongAnswer()
    } 
          
    function plusBet(){
        switch(bet) {      
        case 0:
            bet = 2 ;   
            document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts";
            break;
                
        case 2:
            bet = 4 ;   
            document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts";
            break;

        case 4:
            bet = 8 ;   
            document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts (max)";
            break;        
        default:
    document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts (max)";
    }

        
        console.log("plus!");
    }
          
    function minusBet(){
        switch(bet) {      
        case 2:
            bet = 0 ;   
            document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts";
            break;
                
        case 4:
            bet = 2;   
            document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts";
            break;

        case 8:
            bet = 4;   
            document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts";
            break;        
        default:
        document.getElementById("bet").innerHTML = "Current bet: "+bet+ " pts";
        } 
    }
          
   
</script>    
  </body>
    


    
    
</html>
