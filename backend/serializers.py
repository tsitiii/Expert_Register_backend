from rest_framework import serializers
from django.contrib.auth import authenticate
from django.forms import ValidationError
from django.core.validators import FileExtensionValidator
from . models import ( User,
                    Expert,
                    PersonalDetail,
                    EducationalBackground,
                    WorkExperience,
                    Expertise
                    )

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name','email', 'username','password', 'role', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'password': {'required': True}
        }
        
        
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        data['user'] = user
        return data

def validate_file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File size too large. File size should not exceed 5MB.")

class ExpertSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    cv_file = serializers.FileField(
        required=False,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ]
    )
    class Meta:
        model = Expert
        fields = '__all__'
    def get_country(self, obj):
        return obj.country.name if obj.country else None

    def update(self, instance, validated_data):
        if 'cv_file' in validated_data:
            if instance.cv_file:
                instance.cv_file.delete()
            instance.cv_file = validated_data['cv_file']
        return super().update(instance, validated_data)



class PersonalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetail
        fields = '__all__'
        extra_kwargs = {
            'expert': {'required': False}
        }


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = '__all__'
        extra_kwargs = {
            'expert': {'required': False} 
        }

class WorkExperienceSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=False)
    class Meta:
        model = WorkExperience
        fields = '__all__'
        extra_kwargs = {
            'expert': {'required': False}
        }
        
    def validate(self, data):
        if data.get('end_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                {"end_date": "Must be after start date"}
            )
        return data
    

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'
        extra_kwargs = {
            'expert': {'required': False}
        }


class CVBuilderSerializer(serializers.Serializer):
    expert_id = serializers.IntegerField(required=True)
    personal_detail = PersonalDetailSerializer(required=False)
    education = EducationalBackgroundSerializer(many=True, required=False)
    experience = WorkExperienceSerializer(many=True, required=False)
    expertise = ExpertiseSerializer(required=False)
    
    def validate_expert_id(self, value):
        if not Expert.objects.filter(id=value).exists():
            raise serializers.ValidationError("Expert does not exist")
        return value

    def create(self, validated_data):
        expert = Expert.objects.get(id=validated_data['expert_id'])
        if 'personal_detail' in validated_data:
            PersonalDetail.objects.create(expert=expert, **validated_data['personal_detail'])
        
        if 'education' in validated_data:
            for edu in validated_data['education']:
                EducationalBackground.objects.create(expert=expert, **edu)
        
        if 'experience' in validated_data:
            for exp in validated_data['experience']:
                WorkExperience.objects.create(expert=expert, **exp)
        
        if 'expertise' in validated_data:
            Expertise.objects.create(expert=expert, **validated_data['expertise'])
        
        return expert




