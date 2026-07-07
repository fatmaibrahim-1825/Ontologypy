import setuptools

cdk_version = "1.78.0"

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="scube-ontologypy",
    version="1.0.0",

    description="Project for deploying lambda functions for ontology",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="SCube",

    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),

    install_requires=[
        f"aws-cdk.core=={cdk_version}",
        f"aws-cdk.aws_iam=={cdk_version}",
        f"aws-cdk.aws_ecr=={cdk_version}",
        f"aws-cdk.aws_ssm=={cdk_version}",
        f"aws_cdk.aws_apigateway=={cdk_version}",
        f"aws_cdk.aws_lambda_python=={cdk_version}",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
