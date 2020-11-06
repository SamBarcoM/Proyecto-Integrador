
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
            } );
  </script>
      
  </head>

  <body class="text-center" >
      
      
      
     <nav class="navbar navbar-expand-lg navbar-light bg-light">
         <p>&lt Back</p> 
         <p id="quizName">Quiz - 1</p>
         <p>100 pts</p>

    </nav>
      
      <div id="question-div" class="bg-custom4 question-div">
          <br> 
        <h4 class="h4 mb-4 font-weight-light" id="category">Sports</h4>
          <br>
          <h4 class="h4 mb-4 font-weight-normal" id="question">What is the World Record for 100m freestyle swimming?</h4>
      
          <div class="progress">
            <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
      </div>
      
      
      
    <form class="form-signin" action="" method="post" id="form-question">
        
        <!---Buttons-->
        <input type="submit" class="btn btn-lg btn-block font-weight-light" id="opt0" value="46.91 s">
        <input type="submit" class="btn btn-lg btn-block font-weight-light" id="opt1" value="47.86 s">
        <input type="submit" class="btn btn-lg btn-block font-weight-light" id="opt2" value="45.66 s">
        <input type="submit" class="btn btn-lg btn-block font-weight-light" id="opt3" value="48.05 s">
        
      
    </form>
      
      
   <div class="d-flex p-2">
       <p class="mb-4 font-weight-normal">Current bet: 2 pts</p>
      
      
      
      </div>
      
      <script src="vendor/jquery/jquery-3.5.1.min.js"></script>
      <script src="vendor/bootstrap-4.3.1/js/bootstrap.min.js"></script>
      
      <p class="mt-5 mb-3 text-muted">&copy; COVID-Games 2020</p>
  </body>

    
    
</html>
