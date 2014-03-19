<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">

    <title>Starter Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link href="../../dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="starter-template.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Project name</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">

      <div class="starter-template">

	<img src="/img/Accurator.png">
  <img src="/img/sealinc.png">
	<p>Semi-automated Annotation quality prediction <a href="https://sealincmedia.wordpress.com/" target="_blank">https://sealincmedia.wordpress.com/</a></p>
	<hr>

	%if state == 'start':
	<form action="/trust/upload" method="post" enctype="multipart/form-data">
          Upload Train set: <input type="text" name="name1" />
          <input type="file" name="data1" />
          
          Upload Test set: <input type="text" name="name2" />
          <input type="file" name="data2" />
          <input type="submit" name="submit" value="upload now" />
        </form>

	<div><hr></div>

	<table class="table table-hover">
	  <tr><td><b>Input files</b></td></tr>
	  %for file in inFiles:
	  <tr>
	    <td>{{file}}</td>
	  </tr>
	  %end
	</table>
	<table class="table table-hover">
	  <tr><td><b>Output files</b></td></tr>
	  %for file in outFiles:
	  <tr>
	    <td>{{file}}</td>
	  </tr>
	  %end
	</table>

	%elif state == 'uploaded':
	<form action="/trust/run" method="get">
	  <p>Upload OK</p>
	  <input type="submit" class="btn btn-primary" value="Convert to RDF" />
	</form>

	%else:
	<form action="/trust/download" method="get">
	  <p>TabLinker generated {{numtriples}} triples successfully</p>
	  <input type="submit" class="btn btn-primary" value="Download TTL" />
	  <a href="/trust/home"><input type="button" class="btn btn-primary" value="Start again" /></a>
	</form>
	%end
    
      </div>

    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="//code.jquery.com/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/js/bootstrap.min.js"></script>

  </body>
</html>
