/* eslint react-hooks/exhaustive-deps: "off"*/

import { useCallback, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import { Box, Button, Stack, TextField } from '@mui/material'
import * as THREE from 'three';
import testingMap from './testingMap';

const dimensionsMatrix = [5, 5, 5, 5, 5, 5, 5, 5];

const entireMap = testingMap;

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

const createNewGame = () => {
    
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
    const flattenedMap = entireMap.flat(Infinity);
    const positionMappings = buildScene([0, 0, 0], dimensionsMatrix.length, dimensionsMatrix, entireMap).flat(dimensionsMatrix.length - 1);
    const baseMaterial = new THREE.Material();
    baseMaterial.transparent = true;
    baseMaterial.opacity = .1;

    const [selectedLevelSize, setSelectedLevelSize] = useState(3);
    const [selectedDimNum, setSelectedDimNum] = useState(4);

    const meshRef = useCallback(node => {
        if (node !== null) {
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
        //@
    }, []);

    return (
        <Stack>
            <Box sx={{ width: "100vw", height: "calc(100vh - 75px)", borderBottom: "black 2px solid" }}>
                <Canvas style={{ background: "lightgrey" }}>
                    <instancedMesh ref={meshRef} args={[null, new THREE.MeshBasicMaterial({ transparent: true, opacity: .8, toneMapped: false }), flattenedMap.length]}>
                        <boxGeometry />
                    </instancedMesh>
                    <PerspectiveCamera position={[5, 5, 5]} makeDefault far={2000} />
                    <OrbitControls />
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
                            setSelectedLevelSize(event.target.value);
                        }}
                    />
                    <TextField
                        sx={{ width: 100 }}
                        label="Dimensions"
                        type="number"
                        variant="filled"
                        value={selectedDimNum}
                        onChange={(event) => {
                            setSelectedDimNum(event.target.value);
                        }}
                    />
                </Stack>
            </Box>
        </Stack>
    );
};