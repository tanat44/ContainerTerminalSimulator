using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuayCraneController : MonoBehaviour
{
    const int INITIAL_REACH = 5;
    const int INITIAL_HEIGHT = 8;

    [Header("QC Size")]
    [Range(3, 10)]
    public int maxHeight;


    [Range(3, 10)]
    public int maxReach = INITIAL_REACH;
    Vector3 midFrameOriginalScale;
    

    [Header("Manual control")]
    public bool isManual = true;
    // spreader
    public float spreaderSpeed = 0.02f;
    Vector3 spreaderPosition;
    Vector3 spreaderOriginalPosition;

    // wire
    float wireOriginalLength;
    Vector3 wireOriginalScale;
    Vector3 wireSpreaderOriginalDistance;

    // beam
    Vector3 boomAngle;
    public float boomRotationSpeed = 0.02f;
    Vector3 boomOriginalScale;

    // crane
    Vector3 cranePosition;
    public float craneSpeed = 0.01f;

    GameObject spreader;
    GameObject wire;
    GameObject boom;
    GameObject middleFrame;
    GameObject topFrame;
    GameObject topBackFrame;

    bool ready = false;
    void Start()
    {
        spreader = transform.Find("spreader").gameObject;
        wire = transform.Find("wires").gameObject;
        boom = transform.Find("beam").gameObject;
        middleFrame = transform.Find("qcMid").gameObject;
        topFrame = transform.Find("qcTop").gameObject;
        topBackFrame = transform.Find("qcTopBack").gameObject;

        // spreader
        spreaderPosition = Vector3.zero;
        spreaderOriginalPosition = spreader.transform.localPosition;

        // wire
        wireOriginalScale = wire.transform.localScale;
        wireOriginalLength = topFrame.transform.localPosition.y - spreaderOriginalPosition.y;
        wireSpreaderOriginalDistance = wire.transform.localPosition - spreaderOriginalPosition;

        // beam
        boomAngle = boom.transform.localRotation.eulerAngles;
        boomOriginalScale = boom.transform.localScale;

        // crane
        cranePosition = gameObject.transform.position;

        // resize
        midFrameOriginalScale = middleFrame.transform.localScale;
        ready = true;
    }

    public void ResizeQc(int newHeight, int newReach)
    {
        if (!ready)
            return;
       
        // mid frame
        Vector3 newMidFrameScale = midFrameOriginalScale;
        newMidFrameScale.z *= (float) newHeight / INITIAL_HEIGHT;
        middleFrame.transform.localScale = newMidFrameScale;
        Renderer r = middleFrame.GetComponent<Renderer>();
        Bounds midFrameBound = r.bounds;

        // boom
        Vector3 newBoomScale = boomOriginalScale;
        newBoomScale.y *= (float) newReach / INITIAL_REACH;
        boom.transform.localScale = newBoomScale;
        Vector3 newBoomPos = boom.transform.localPosition;
        newBoomPos.y = midFrameBound.max.y;
        boom.transform.localPosition = newBoomPos;

        // top frame
        Vector3 newTopFramePos = topFrame.transform.localPosition;
        newTopFramePos.y = midFrameBound.max.y;
        topFrame.transform.localPosition = newTopFramePos;

        // top back frame
        Vector3 newTopBackFramePos = topBackFrame.transform.localPosition;
        newTopBackFramePos.y = midFrameBound.max.y;
        topBackFrame.transform.localPosition = newTopBackFramePos;

        maxHeight = newHeight;
        maxReach = newReach;
    }

    void Update()
    {
        if (isManual)
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
            }
            if (Input.GetKey(KeyCode.A))
            {
                spreaderPosition.z += spreaderSpeed;
            }
            if (Input.GetKey(KeyCode.R))
            {
                boomAngle.x += boomRotationSpeed;
                if (boomAngle.x < 0)
                {
                    boomAngle.x = 0;
                }
            }
            if (Input.GetKey(KeyCode.F))
            {
                boomAngle.x -= boomRotationSpeed;
                if (boomAngle.x > 90)
                {
                    boomAngle.x = 90;
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

            if (Input.GetKey(KeyCode.LeftControl))
            {
                ResizeQc(6, 6);
            }
        }

        MoveSpreader(spreaderPosition);

        // beam
        boom.transform.localRotation = Quaternion.Lerp(boom.transform.localRotation, Quaternion.Euler(boomAngle), Time.time);

        // crane
        gameObject.transform.position = Vector3.Lerp(gameObject.transform.position, cranePosition, Time.time);

    }

    void MoveSpreader(Vector3 newPosition)
    {
        // spreader pos
        Vector3 newSpreaderPos = newPosition + spreaderOriginalPosition;
        spreader.transform.localPosition = Vector3.Lerp(spreader.transform.localPosition, newSpreaderPos, Time.time);

        // wire pos
        wire.transform.localPosition = Vector3.Lerp(wire.transform.localPosition, newSpreaderPos + wireSpreaderOriginalDistance, Time.time);

        // wire scale
        float newLength = topFrame.transform.localPosition.y - newSpreaderPos.y;
        Vector3 newWireScale = wireOriginalScale;
        newWireScale.z = newLength / wireOriginalLength * wireOriginalScale.z;
        wire.transform.localScale = newWireScale;
    }

    private void OnValidate()
    {
        ResizeQc(maxHeight, maxReach);
    }
}
