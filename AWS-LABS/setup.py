import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="aws_labs",
    version="0.0.1",

    description="KHLABS : AWS LABS CDK APP",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Kh B.",

    package_dir={"": "aws_labs"},
    packages=setuptools.find_packages(where="aws_labs"),

    install_requires=[
        "aws-cdk.core==1.116.0",
        "aws_cdk.aws_ec2==1.116.0",
        "aws_cdk.aws_elasticloadbalancingv2==1.116.0",
        "aws_cdk.aws_autoscaling==1.116.0",
        "aws_cdk.aws_lambda==1.116.0",
        "aws_cdk.aws_secretsmanager==1.116.0",
        "aws-cdk.aws_wafv2==1.116.0",
        "aws-cdk.aws-s3==1.116.0"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

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
