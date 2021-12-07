using UnityEngine;
using System.Collections;


[AddComponentMenu("Camera-Control/3dsMax Camera Style")]
public class CameraOrbit : MonoBehaviour
{
    public Vector3 targetOffset;

    public float xSpeed = 200.0f;
    public float ySpeed = 200.0f;
    public int yMinLimit = 0;
    public int yMaxLimit = 80;
    public int zoomRate = 40;
    public float panSpeed = 0.3f;
    public float zoomDampening = 5.0f;

    private const float MIN_Y = 5.0f;
    private float xDeg = 0.0f;
    private float yDeg = 0.0f;
    private float desiredDistance;
    private float wheelValue = 0.0f;
    private Quaternion currentRotation;
    private Quaternion desiredRotation;
    private Transform initial;

    void Start() { Init(); }
    void OnEnable() { Init(); }

    public void Init()
    {
        initial = transform;
        //be sure to grab the current rotations as starting points.
        currentRotation = transform.rotation;
        desiredRotation = transform.rotation;

        xDeg = Vector3.Angle(Vector3.right, transform.right);
        yDeg = Vector3.Angle(Vector3.up, transform.up);

        wheelValue = Input.GetAxis("Mouse ScrollWheel");
    }

    /*
     * Camera logic on LateUpdate to only update after all character movement logic has been handled. 
     */
    void LateUpdate()
    {
        // MIDDLE MOUSE: ORBIT
        if (Input.GetMouseButton(2))
        {
            xDeg += Input.GetAxis("Mouse X") * xSpeed * 0.02f;
            yDeg -= Input.GetAxis("Mouse Y") * ySpeed * 0.02f;

            ////////OrbitAngle

            //Clamp the vertical axis for the orbit
            yDeg = ClampAngle(yDeg, yMinLimit, yMaxLimit);
            // set camera rotation 
            desiredRotation = Quaternion.Euler(yDeg, xDeg, 0);
            currentRotation = transform.rotation;
            transform.rotation = Quaternion.Lerp(currentRotation, desiredRotation, Time.deltaTime * zoomDampening);
        }
        // RIGHTMOUSE : PAN by way of transforming the target in screenspace
        else if (Input.GetMouseButton(1))
        {
            //grab the rotation of the camera so we can move in a psuedo local XY space
            transform.Translate(Vector3.right * -Input.GetAxis("Mouse X") * panSpeed);
            transform.Translate(transform.up * -Input.GetAxis("Mouse Y") * panSpeed, Space.World);
        }

        // SCROLLWHEEL : ZOOM
        desiredDistance -= (Input.GetAxis("Mouse ScrollWheel")-wheelValue) * zoomRate;
        transform.position = transform.position - (transform.rotation * Vector3.forward * desiredDistance + targetOffset);

        // not allow camera to dive underground (y<0)
        Vector3 p = transform.position;
        if (p.y < MIN_Y)
        {
            p.y = MIN_Y;
            transform.position = p;
        }

        wheelValue = Input.GetAxis("Mouse ScrollWheel");
    }

    private static float ClampAngle(float angle, float min, float max)
    {
        if (angle < -360)
            angle += 360;
        if (angle > 360)
            angle -= 360;
        return Mathf.Clamp(angle, min, max);
    }
    public void Reset()
    {
        transform.position = initial.position;
        transform.rotation = initial.rotation;

        Init();
    }
}