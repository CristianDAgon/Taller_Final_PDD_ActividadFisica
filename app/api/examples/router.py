from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_examples():
    return {
        "iteratives": ["sumatoria.txt", "burbuja.txt"],
        "recursive": ["factorial.txt", "mergesort.txt"],
    }
