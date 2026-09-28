#!/bin/bash
cd "$(dirname "$0")"
export BLENDER_USER_RESOURCES=$PWD/blres
run() { ../bl/bin/python build.py "$1" 2>&1 | grep -E "exported|rror|Traceback"; }
run '{"out":"m_young","gender":1.0,"age":0.45,"muscle":0.6,"weight":0.5,"hair":"short02","brow":"eyebrow001","outfit":"peasant_m"}'
run '{"out":"m_heavy","gender":1.0,"age":0.62,"muscle":0.5,"weight":0.85,"hair":"short04","brow":"eyebrow003","outfit":"peasant_m"}'
run '{"out":"m_old","gender":1.0,"age":0.9,"muscle":0.35,"weight":0.5,"height":0.4,"hair":"short03","brow":"eyebrow006","outfit":"peasant_m"}'
run '{"out":"f_young","gender":0.0,"age":0.42,"muscle":0.45,"weight":0.45,"hair":"braid01","brow":"eyebrow012","outfit":"peasant_f"}'
run '{"out":"f_mid","gender":0.0,"age":0.62,"muscle":0.4,"weight":0.72,"hair":"ponytail01","brow":"eyebrow009","outfit":"peasant_f"}'
run '{"out":"f_old","gender":0.0,"age":0.9,"muscle":0.3,"weight":0.55,"height":0.35,"hair":"bob02","brow":"eyebrow011","outfit":"peasant_f"}'
run '{"out":"boy","gender":1.0,"age":0.16,"muscle":0.5,"weight":0.45,"hair":"short01","brow":"eyebrow002","outfit":"peasant_m"}'
run '{"out":"girl","gender":0.0,"age":0.16,"muscle":0.5,"weight":0.45,"hair":"long01","brow":"eyebrow004","outfit":"peasant_f"}'
echo CAST DONE
