using System.Collections;
using System.Collections.Generic;
using UnityEditor.Scripting.Python;
using UnityEditor;
public class littleDance : UnityEngine.MonoBehaviour
{
        [MenuItem("Python/Hello World")]

    public void OnItemClicked()
    {
        PythonRunner.RunString(@"
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):
    # Turn 90 degrees to the left.
    # Note: To turn to the right, just use a negative number.
    robot.turn_in_place(degrees(-30)).wait_for_completed()
    robot.turn_in_place(degrees( 30)).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabAmazed).wait_for_completed()

cozmo.run_program(cozmo_program)
");
    }
}