Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get install python-software-properties -y
    sudo add-apt-repository ppa:fkrull/deadsnakes -y
    sudo apt-get update
    sudo apt-get install -y build-essential libxslt1-dev libxml2-dev python-dev python3-dev libz-dev python3.3 python3.4 python3.3-dev python3.4-dev python-sphinx
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
  SHELL
end
