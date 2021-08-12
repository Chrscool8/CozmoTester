using System.Collections;
using System.Collections.Generic;
using UnityEditor.Scripting.Python;
using UnityEditor;
public class sayHello : UnityEngine.MonoBehaviour
{
[MenuItem("Python/Hello World")]
    public void OnItemClicked()
    {
        PythonRunner.RunString(@"
import cozmo

def cozmo_program(robot: cozmo.robot.Robot):
    robot.say_text('Hello Digital Dream Labs').wait_for_completed()

cozmo.run_program(cozmo_program)");
    }
}