using System.Collections;
using System.Collections.Generic;
using UnityEditor.Scripting.Python;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public class PyAgain : UnityEngine.MonoBehaviour
{
    public bool activated = false;
    public void OnItemClicked()
    {
        if (!activated)
        {
            activated = true;
            Debug.Log("Clicked Click");
            GameObject.Find("Button_Start").GetComponentInChildren<Text>().text = "Started";

            /*PythonRunner.RunString(@"
import cozmo
import UnityEngine;
UnityEngine.Debug.Log('hello world')

def cozmo_program(robot: cozmo.robot.Robot):
    robot.move_head(5)
    robot.say_text('Hello Digital Dream Labs!').wait_for_completed()
    robot.move_head(-5)

cozmo.run_program(cozmo_program)");*/

            //PythonRunner.RunFile("Assets/UdpComms.py");
            PythonRunner.RunFile("Assets/server.py");
        }
    }
}