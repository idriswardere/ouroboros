/* eslint react-hooks/exhaustive-deps: "off"*/

import { useCallback, useState, useEffect, useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import { Box, Button, Stack, TextField } from '@mui/material'
import * as THREE from 'three';
import axios from 'axios';
import testingMap from './testingMap';


const baseInstance = axios.create({
    baseURL: "http://localhost:5000/",
    timeout: undefined
});

const determineColor = (state) => {
    if (state === -1) { //fruit
        return 0xff0000;
    } else if (state === -2) { //wall
        return 0x18191c;
    } else if (state === 1) { //head
        return 0x0ac9c3;
    } else if (state === 2) { //body
        return 0x4c63e6;
    } else { //empty
        return 0xffffff;
    }

}

const buildScene = (position, currentDimension, dimensionsMatrix, map) => {
    const dimensionLevel = Math.floor((currentDimension - 1) / 3);
    let spacing = 1.5;
    if (dimensionLevel > 0) {
        let subCubes = 1;
        dimensionsMatrix.forEach((numCubes, index) => {
            if (index < currentDimension - 1 && index % 3 === (currentDimension - 1) % 3) {
                subCubes = subCubes * (numCubes + 1);
            }
        });
        spacing = spacing * Math.max(subCubes, 1);
    }

    if (currentDimension === 0) {
        return position;
    }
    return map.map((subMap) => {
        if (currentDimension % 3 === 0) { //change z axis
            position[2] += spacing;
        } else if (currentDimension % 2 === 0) { //change y axis
            position[1] += spacing;
        } else { //change x axis
            position[0] += spacing;
        }
        return buildScene([...position], currentDimension - 1, dimensionsMatrix, subMap);
    });
}

export default function Scene() {

    const controlsRef = useRef();

    const [entireMap, setEntireMap] = useState(testingMap);
    const [flattenedMap, setFlattenedMap] = useState(entireMap.flat(Infinity));
    const [positionMappings, setPositionMappings] = useState();
    const [dimensionsMatrix, setDimensionsMatrix] = useState([5, 5, 5, 5, 5, 5, 5, 5]);
    const flattenedMapRef = useRef();

    const [lastDirectionalInput, setLastDirectionalInput] = useState(1);
    const [dimGroup, setDimGroup] = useState(1);
    const lastDirectionalInputRef = useRef();
    const dimGroupRef = useRef();

    const gameStartedRef = useRef(false);
    const meshReference = useRef();

    const baseMaterial = new THREE.Material();
    baseMaterial.transparent = true;
    baseMaterial.opacity = .1;

    const [selectedLevelSize, setSelectedLevelSize] = useState(3);
    const [selectedDimNum, setSelectedDimNum] = useState(4);

    const handleUserInput = (event) => {
        switch (event.key) {
            case 'q': //z axis, 3, 6, 9, etc.
                setLastDirectionalInput((3 * dimGroupRef.current) - 1);
                break;
            case 'e':
                setLastDirectionalInput(((3 * dimGroupRef.current) - 1) * -1);
                break;
            case 'w': //y axis, 2, 5, 8, etc.
                setLastDirectionalInput(((3 * dimGroupRef.current) - 2) * -1);
                break;
            case 's':
                setLastDirectionalInput((3 * dimGroupRef.current) - 2);
                break;
            case 'a': //x axis, 1, 4, 7, etc.
                setLastDirectionalInput(3 * dimGroupRef.current * -1);
                break;
            case 'd':
                setLastDirectionalInput(3 * dimGroupRef.current);
                break;
            default:
                break;
        }
    }

    const handleCtrlKeyDown = (event) => {
        if (event.repeat) { return }
        if (event.key === "Control" && controlsRef?.current != null) {
            controlsRef.current.enableZoom = false;
        }
    }

    const handleCtrlKeyUp = (event) => {
        if (event.repeat) { return }
        if (event.key === "Control" && controlsRef?.current != null) {
            controlsRef.current.enableZoom = true;
        }
    }

    const handleUserScroll = (event) => {
        if (event.ctrlKey) {
            event.preventDefault();
            if (event.deltaY > 0) { //scroll down        
                setDimGroup((prevState) => prevState - 1);
            } else { //scroll up
                setDimGroup((prevState) => prevState + 1);
            }
        }
    }

    const handleSnakeMove = () => {
        if (gameStartedRef.current) {
            baseInstance.get("/progress/" + lastDirectionalInputRef.current).then((data) => {
                if (data?.data?.diff) {
                    if (data.data.status > 0) {
                        gameStartedRef.current = false;
                    }
                    Object.keys(data.data.diff).forEach((key) => {
                        flattenedMapRef.current[parseInt(key)] = data.data.diff[key];
                    });
                    setFlattenedMap([...flattenedMapRef.current]);
                }

            }).catch((e) => console.error(e));
        }
    }

    useEffect(() => {
        window.addEventListener("keypress", handleUserInput);
        window.addEventListener("keydown", handleCtrlKeyDown);
        window.addEventListener("keyup", handleCtrlKeyUp);
        window.addEventListener("wheel", handleUserScroll, { passive: false });
        const intervalId = window.setInterval(handleSnakeMove, 1000);
        return () => {
            window.removeEventListener('keypress', handleUserInput);
            window.removeEventListener('keydown', handleCtrlKeyDown);
            window.addEventListener("keyup", handleCtrlKeyUp);
            window.removeEventListener('wheel', handleUserScroll);
            clearInterval(intervalId);
        };
    }, []);

    useEffect(() => {
        flattenedMapRef.current = flattenedMap;
    }, [flattenedMap]);

    useEffect(() => {
        setFlattenedMap(entireMap.flat(Infinity));
        setPositionMappings(buildScene([0, 0, 0], dimensionsMatrix.length, dimensionsMatrix, entireMap).flat(dimensionsMatrix.length - 1));
    }, [entireMap]);

    const createNewGame = () => {
        baseInstance.get("/init/" + selectedLevelSize + "/" + selectedDimNum).then((data) => {
            setEntireMap(data.data.state);
            setDimensionsMatrix(new Array(selectedDimNum).fill(selectedLevelSize));
            gameStartedRef.current = true;
        }).catch((e) => console.error(e));
    }

    useEffect(() => {
        dimGroupRef.current = dimGroup;
    }, [dimGroup]);

    useEffect(() => {
        lastDirectionalInputRef.current = lastDirectionalInput;
    }, [lastDirectionalInput]);

    const meshRef = useCallback(node => {
        if (node !== null) {
            meshReference.current = node;

            const tempObject = new THREE.Object3D();

            flattenedMap.forEach((state, index) => {
                tempObject.position.set(positionMappings[index][0], positionMappings[index][1], positionMappings[index][2]);
                node.setColorAt(index, new THREE.Color(determineColor(state)));
                tempObject.scale.set(1, 1, 1);
                tempObject.updateMatrix();
                node.setMatrixAt(index, tempObject.matrix);
            });

            node.instanceMatrix.needsUpdate = true;
            node.instanceColor.needsUpdate = true;
        }
    }, [flattenedMap]);

    return (
        <Stack>
            <Box sx={{ width: "100vw", height: "calc(100vh - 75px)", borderBottom: "black 2px solid" }}>
                <Canvas style={{ background: "lightgrey" }}>
                    <instancedMesh ref={meshRef} args={[null, new THREE.MeshBasicMaterial({ transparent: true, opacity: .2, toneMapped: false }), flattenedMap.length]}>
                        <boxGeometry />
                    </instancedMesh>
                    <PerspectiveCamera position={[5, 5, 5]} makeDefault far={2000} />
                    <OrbitControls ref={controlsRef} />
                </Canvas>
            </Box>
            <Box sx={{ width: "100vw", height: 75 - 2 }}>
                <Stack direction="row" sx={{ m: 1, height: 75 - 2 - 16 }} spacing={1}>
                    <Button variant='contained' size="large" onClick={createNewGame}>
                        Start
                    </Button>
                    <TextField
                        sx={{ width: 100 }}
                        label="Level Size"
                        type="number"
                        variant="filled"
                        value={selectedLevelSize}
                        onChange={(event) => {
                            setSelectedLevelSize(parseInt(event.target.value));
                        }}
                    />
                    <TextField
                        sx={{ width: 100 }}
                        label="Dimensions"
                        type="number"
                        variant="filled"
                        value={selectedDimNum}
                        onChange={(event) => {
                            setSelectedDimNum(parseInt(event.target.value));
                        }}
                    />
                </Stack>
            </Box>
        </Stack>
    );
};