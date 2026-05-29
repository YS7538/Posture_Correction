##Threading:- 
    Learnt to implement multi threading using python because while using playsound the main loop and callback was freezing so put that in another thread to run simultaneously.
##Pathlib:- 
    Pathlib returns path as its output which works totally fine with newer functions but older ones like Mediapipe that we used here, expects path in a string format so before passing convert the output to str.