import smartthings_settings as settings

main_page='''
<!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

  <script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65257509-1', 'auto');
  ga('send', 'pageview');

</script>

</head>





<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://alexa.zpriddy.com">ZP Alexa Projects</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="https://alexa.zpriddy.com">Home <span class="sr-only">(current)</span></a></li>
        <li><a href="#">SmartThings</a></li>
        <li><a href="https://alexa.zpriddy.com/nest">Nest</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="https://zpriddy.com">zpriddy.com</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>



<div class="container">

<div class="row">
<div class="col-md-2"></div>
<div class="col-md-8">
		<div class="jumbotron">
		    <h2> Help Me Out!</h2>
		  </div>
	    <p>Please consider helping me out so that I can keep supporting this and other Open Source projects! I run all of this out of my pocket and it doesnt all come free.. Please consider helping me out so that I can keep everything running!
	    </p>
	    <p><a class="btn btn-primary btn-lg" href="https://cash.me/$ZPriddy" role="button">Donate via Square Cash!</a></p>
	</div>
<div class="col-md-2"></div>
</div>

<div class="container">
	<div class="panel panel-default">
		<div class="panel-heading">
		    <h3 class="panel-title">Setting up Alexa with your SmartThings</h3>
		  </div>
		  <div class="panel-body">

		  To setup your Alexa to talk to SmartThings please go to my Github linked below and follow the README instructions. There are three other files that you will need in order to complete the process (Thats why I link to Github).

		<a class="btn btn-warning" href="https://github.com/zpriddy/ZP-Echo-ST-Beta" role="button">Git Hub</a>

		
		</div>
	</div>
	<div class="panel panel-default">
		<div class="panel-heading">
		    <h3 class="panel-title">Quick Links</h3>
		  </div>
		  <div class="panel-body">

		<a class="btn btn-success" href="{0}/auth" role="button">SmartThings Alexa Auth</a>
		<a class="btn btn-info" href="{0}/samples" role="button">SmartThings Alexa Smaples</a>
		</div>
	</div>
</div>
 </div>


'''

auth_page='''
<!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

  <script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65257509-1', 'auto');
  ga('send', 'pageview');

</script>


</head>





<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://alexa.zpriddy.com">ZP Alexa Projects</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li><a href="https://alexa.zpriddy.com">Home</a></li>
        <li class="active"><a href="#">SmartThings<span class="sr-only">(current)</span></a></li>
        <li><a href="#">Nest</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="https://zpriddy.com">zpriddy.com</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<div class="container">




<form action="auth" method="post">
<div class="form-group">
	<label for="AlexaID">Alexa ID</label>
	<input id="AlexaID" name="AlexaID" type="text" class="form-control" title="Alexa ID. This is a required field">
</div>
<div class="form-group">
	<label for="SmartThingsClientID">SmartThings Client ID</label>
	<input id="SmartThingsClientID" name="SmartThingsClientID" type="text" class="form-control" title="SmartThings Client ID. This is a required field">
</div>
<div class="form-group">
	<label for="SmartThingsClientSecret">SmartThings Client Secret </label>
	<input id="SmartThingsClientSecret" name="SmartThingsClientSecret" type="text" class="form-control" title="SmartThings Client Secret . This is a required field">
</div>
<input type="submit" value="Authorize" class="btn btn-default">
</form>
</div>
'''

nest_page='''
<!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

  <script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65257509-1', 'auto');
  ga('send', 'pageview');

</script>

</head>





<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://alexa.zpriddy.com">ZP Alexa Projects</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li><a href="https://alexa.zpriddy.com">Home</a></li>
        <li><a href="#">SmartThings</a></li>
        <li class="active"><a href="https://alexa.zpriddy.com/nest">Nest <span class="sr-only">(current)</span></a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="https://zpriddy.com">zpriddy.com</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>



<div class="container">

<div class="row">
<div class="col-md-2"></div>
<div class="col-md-8">
    <div class="jumbotron">
        <h2> Help Me Out!</h2>
      </div>
      <p>Please consider helping me out so that I can keep supporting this and other Open Source projects! I run all of this out of my pocket and it doesnt all come free.. Please consider helping me out so that I can keep everything running!
      </p>
      <p><a class="btn btn-primary btn-lg" href="https://cash.me/$ZPriddy" role="button">Donate via Square Cash!</a></p>
  </div>
<div class="col-md-2"></div>
</div>

<div class="container">
  <div class="panel panel-default">
    <div class="panel-heading">
        <h3 class="panel-title">Setting up Nest with your SmartThings</h3>
      </div>
      <div class="panel-body">

      Comming Soon


    
    </div>
  </div>
  <div class="panel panel-default">
    <div class="panel-heading">
        <h3 class="panel-title">Quick Links</h3>
      </div>
      <div class="panel-body">

    <a class="btn btn-success" href="https://alexa.zpriddy.com/alexa/auth" role="button">SmartThings Alexa Auth</a>
    <a class="btn btn-info" href="https://alexa.zpriddy.com/alexa/samples" role="button">SmartThings Alexa Smaples</a>
    </div>
  </div>
</div>
 </div>


'''


samples_page='''
<!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

  <script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65257509-1', 'auto');
  ga('send', 'pageview');

</script>


</head>





<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://alexa.zpriddy.com">ZP Alexa Projects</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li><a href="https://alexa.zpriddy.com">Home</a></li>
        <li class="active"><a href="#">SmartThings<span class="sr-only">(current)</span></a></li>
        <li><a href="#">Nest</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="https://zpriddy.com">zpriddy.com</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<div class="container">




<form action="samples" method="post">
<div class="form-group">
	<label for="AlexaID">Alexa ID</label>
	<input id="AlexaID" name="AlexaID" type="text" class="form-control" title="Alexa ID. This is a required field">
</div>
<input type="submit" value="Get Samples" class="btn btn-default">
</form>
</div>
'''

samples_results='''
<!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

  <script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65257509-1', 'auto');
  ga('send', 'pageview');

</script>

</head>





<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://alexa.zpriddy.com">ZP Alexa Projects</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li><a href="https://alexa.zpriddy.com">Home</a></li>
        <li class="active"><a href="#">SmartThings<span class="sr-only">(current)</span></a></li>
        <li><a href="#">Nest</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="https://zpriddy.com">zpriddy.com</a></li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<div class="container">
<h1>Sample Resultss</h1>
<p> Please copy and paste the results below into your Alexa SampleUtterances in the ASK portal. </p>
<div class="panel panel-primary">
        <div class="panel-heading">Sample</div>
              <div class="panel-body" style="max-height: 10;overflow-y: scroll;">RESULTS</div>
        </div>
  </div>

</div>
'''
NotNestUser = {"outputSpeech": {"type":"PlainText","text":"Current user is not a valid nest user. Please look for help"},"card":{"type":"Simple","title":"Nest Control Error","content":"Current user is not a valid nest user. Please look for help"},'shouldEndSession':True}