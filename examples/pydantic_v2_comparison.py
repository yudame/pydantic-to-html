"""
Example comparing Pydantic v2 dataclasses vs. BaseModel classes
"""
import dataclasses
import json
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, ValidationError
from pydantic.dataclasses import dataclass


# BaseModel example
class UserModel(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(gt=0, description="User's age")
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)


# Pydantic dataclass example
@dataclass
class UserDataclass:
    name: str = Field(description="User's full name")
    age: int = Field(gt=0, description="User's age")
    tags: List[str] = dataclasses.field(default_factory=list)
    metadata: Dict[str, str] = dataclasses.field(default_factory=dict)


def main():
    # Create instances
    model_user = UserModel(name="Alice", age=30, tags=["staff"])
    dataclass_user = UserDataclass(name="Bob", age=28, tags=["customer"])
    
    print("=== Instance Creation ===")
    print(f"BaseModel instance: {model_user}")
    print(f"Dataclass instance: {dataclass_user}")
    
    # Accessing data
    print("\n=== Data Access ===")
    print(f"BaseModel to dict: {model_user.model_dump()}")
    print(f"Dataclass to dict: {dataclasses.asdict(dataclass_user)}")
    
    # Schema generation
    print("\n=== Schema Generation ===")
    print(f"BaseModel has schema: {hasattr(UserModel, 'model_json_schema')}")
    if hasattr(UserModel, 'model_json_schema'):
        print(f"Schema: {json.dumps(UserModel.model_json_schema(), indent=2)[:150]}...")
    
    print(f"Dataclass has schema: {hasattr(UserDataclass, 'model_json_schema')}")
    # Pydantic dataclasses don't have model_json_schema directly on the class
    
    # Field metadata
    print("\n=== Field Metadata Access ===")
    print(f"BaseModel fields: {list(UserModel.model_fields.keys())}")
    print(f"BaseModel field type: {type(UserModel.model_fields['name'])}")
    print(f"Dataclass fields: {list(UserDataclass.__pydantic_fields__.keys())}")
    
    # Validation methods
    print("\n=== Validation Methods ===")
    print(f"BaseModel model_validate: {hasattr(UserModel, 'model_validate')}")
    
    # Let's use the model_validate method
    data = {"name": "Charlie", "age": 42, "tags": ["vip"]}
    validated_model = UserModel.model_validate(data)
    print(f"Validated model: {validated_model}")
    
    try:
        # Invalid data (negative age)
        UserModel.model_validate({"name": "Dana", "age": -5})
    except ValidationError as e:
        print(f"BaseModel validation error: {e.errors()[0]['type']}")
        
    try:
        # Invalid dataclass (negative age)
        UserDataclass(name="Dana", age=-5)
    except ValidationError as e:
        print(f"Dataclass validation error: {e.errors()[0]['type']}")


if __name__ == "__main__":
    main()