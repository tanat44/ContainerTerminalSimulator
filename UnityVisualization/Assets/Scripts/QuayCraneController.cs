using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuayCraneController : MonoBehaviour
{
    GameObject spreader;
    GameObject spreaderWires;
    GameObject beam;

    // spreader
    Vector3 spreaderPosition;
    public float spreaderSpeed = 0.02f;

    // wire
    Vector3 spreaderWirePosition;
    float originalWireLength;
    Vector3 originalWireScale;
    float originalWireY;

    // beam
    Vector3 beamAngle;
    public float beamRotationSpeed = 0.02f;

    // crane
    Vector3 cranePosition;
    public float craneSpeed = 0.01f;
    void Start()
    {
        spreader = transform.Find("spreader").gameObject;
        spreaderWires = transform.Find("wires").gameObject;
        beam = transform.Find("beam").gameObject;

        // spreader
        spreaderPosition = spreader.transform.localPosition;

        // wire
        spreaderWirePosition = spreaderWires.transform.localPosition;
        originalWireScale = spreaderWires.transform.localScale;
        originalWireLength = spreaderWires.transform.position.y - spreader.transform.position.y;
        originalWireY = spreaderWires.transform.position.y;

        // beam
        beamAngle = beam.transform.localRotation.eulerAngles;

        // crane
        cranePosition = gameObject.transform.position;
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            spreaderPosition.y += spreaderSpeed;
        }
        if (Input.GetKey(KeyCode.S))
        {
            spreaderPosition.y -= spreaderSpeed;
        }
        if (Input.GetKey(KeyCode.D))
        {
            spreaderPosition.z -= spreaderSpeed;
            spreaderWirePosition.z -= spreaderSpeed;
        }
        if (Input.GetKey(KeyCode.A))
        {
            spreaderPosition.z += spreaderSpeed;
            spreaderWirePosition.z += spreaderSpeed;
        }
        if (Input.GetKey(KeyCode.R))
        {
            beamAngle.x += beamRotationSpeed;
            if (beamAngle.x < 0)
            {
                beamAngle.x = 0;
            }
        }
        if (Input.GetKey(KeyCode.F))
        {
            beamAngle.x -= beamRotationSpeed;
            if (beamAngle.x > 90)
            {
                beamAngle.x = 90;
            }
        }

        if (Input.GetKey(KeyCode.X))
        {
            cranePosition += craneSpeed * gameObject.transform.right;
        }
        if (Input.GetKey(KeyCode.Z))
        {
            cranePosition -= craneSpeed * gameObject.transform.right;
        }

        // spreader
        spreader.transform.localPosition = Vector3.Lerp(spreader.transform.localPosition, spreaderPosition, Time.time);

        // wire
        Vector3 newWirePosition = spreaderWires.transform.localPosition;
        spreaderWires.transform.localPosition = Vector3.Lerp(spreaderWires.transform.localPosition, spreaderWirePosition, Time.time);
        float newWireLength = originalWireY - spreader.transform.position.y;
        float newScale = originalWireScale.z / originalWireLength * newWireLength;
        Vector3 newWireScale = originalWireScale;
        newWireScale.z = newScale;
        spreaderWires.transform.localScale = newWireScale;

        // beam
        beam.transform.localRotation = Quaternion.Lerp(beam.transform.localRotation, Quaternion.Euler(beamAngle), Time.time);

        // crane
        gameObject.transform.position = Vector3.Lerp(gameObject.transform.position, cranePosition, Time.time);
        
    }
}
