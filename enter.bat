mode con cols=15 lines=1

if "%1" == "h" goto begin
	mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
	:begin

python ./enter_chrome.py
