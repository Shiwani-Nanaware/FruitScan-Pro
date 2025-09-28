<?php
class Person
{
	public $name;
	public $age;
	function set_info($name,$age)
	{
		$this->name=$name;
		$this->age=$age;
	}
	function display_info()
	{
		echo "Name: ".$this->$name."";
		echo "Age: ".$this->$age."";
	}
}
class Student extends Person
{
	public $grade;
	function setStudentInfo($name,$age,$grade)
	{
		$this->grade=$grade;
	}
	function dislaystudentinfo()
	{
		echo "Grade: ".$this->$grade."";
	}
}
$s=new Student()
$s->setStudentInfo("shiwani",18,'A');
$s->displaystudentinfo();

?>