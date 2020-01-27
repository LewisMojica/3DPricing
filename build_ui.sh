pre_dir=$(pwd);
cd UI;

pyuic5 gui.ui -o MainW.py;
pyuic5 _3dpricing_dialog.ui -o _3dpricing_dialog.py;
pyuic5 licence_dialog.ui -o licence_dialog.py;
pyuic5 source_code_dialog.ui -o source_code_dialog.py;
pyuic5 settings.ui -o settings.py;
pyuic5 init_dialog.ui -o init_dialog.py;
pyuic5 config_error.ui -o config_error.py;


cd $pre_dir;