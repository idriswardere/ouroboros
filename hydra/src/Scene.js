import { useEffect, useState, useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import { Box } from '@mui/material'
import * as THREE from 'three';

//currently hardcoded to 3
const dimensionsMatrix = [3, 3, 3, 3, 3, 3];

const entireMap = [
    [
        [
            [
                [
                    [1, 2, 2],
                    [0, -2, 2],
                    [0, 0, 2],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ],
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ],
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ]
    ],
    [
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ],
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ],
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ]
    ],
    [
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ],
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ],
        [
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            [
                [
                    [0, 0, 0],
                    [0, -2, 0],
                    [0, 0, 0],
                ],
                [
                    [-2, 0, -1],
                    [-2, 0, 0],
                    [-2, -2, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ]
        ]
    ],
];

const determineColor = (state) => {
    if (state == -1) { //fruit
        return "#ff0000";
    } else if (state == -2) { //wall
        return "#18191c";
    } else if (state == 1) { //head
        return "#0ac9c3";
    } else if (state == 2) { //body
        return "#4c63e6";
    } else { //empty
        return "#ffffff";
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
    return map.map((subMap, index) => {
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

function Cell({ state, position }) {
    const color = determineColor(state);

    return (
        <>
            <mesh position={position}>
                <boxGeometry />
                <meshStandardMaterial color={color} />
            </mesh>
        </>
    );

}

export default function Scene() {

    const positionMappings = buildScene([0, 0, 0], dimensionsMatrix.length, dimensionsMatrix, entireMap).flat(dimensionsMatrix.length - 1);
    const flattenedMap = entireMap.flat(Infinity);

    console.log(positionMappings);

    return (
        <Box sx={{ width: "100vw", height: "calc(100vh - 100px)", borderBottom: "black 2px solid" }}>
            <Canvas>
                <PerspectiveCamera position={[5, 5, 5]} makeDefault />
                <ambientLight intensity={Math.PI / 2} />
                <spotLight position={[100, 100, 150]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
                <pointLight position={[100, 100, 150]} decay={0} intensity={Math.PI} />
                <OrbitControls />
                {flattenedMap.map((state, index) => <Cell key={positionMappings[index]} state={state} position={positionMappings[index]} />)}
            </Canvas>
        </Box>
    );
};